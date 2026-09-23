"""
CodeCraftHub - Simple Flask REST API for tracking learning courses.

Run this file with:
    python app.py

The API will be available at:
    http://127.0.0.1:5000
"""

from flask import Flask, jsonify, request
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import re
import tempfile


app = Flask(__name__)

# Path to the JSON file used as our simple data storage.
DATA_FILE = Path("courses.json")

# The only valid values allowed for a course status.
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]

# YYYY-MM-DD format pattern.
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def ensure_data_file_exists():
    """
    Create courses.json with an empty list if it does not already exist.
    """
    if not DATA_FILE.exists():
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=2)
        except OSError as error:
            # This is printed to the terminal because the app cannot continue
            # correctly if it cannot create its storage file.
            print(f"Error creating {DATA_FILE}: {error}")


def read_courses():
    """
    Read all courses from courses.json.

    Returns:
        tuple: (courses, error_message)

        - courses is a list when successful.
        - error_message is None when successful.
        - If an error occurs, courses will be None and error_message
          will contain a helpful message.
    """
    ensure_data_file_exists()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            courses = json.load(file)

        # The JSON file should always contain a list of course objects.
        if not isinstance(courses, list):
            return None, "Invalid courses.json format. Expected a JSON list."

        return courses, None

    except json.JSONDecodeError:
        return None, "courses.json contains invalid JSON."
    except OSError as error:
        return None, f"Unable to read courses.json: {error}"


def write_courses(courses):
    """
    Save the complete list of courses to courses.json.

    A temporary file is used first, then replaced with courses.json.
    This helps reduce the chance of leaving a partially-written JSON file.

    Returns:
        tuple: (success, error_message)
    """
    temp_file_name = None

    try:
        # Create a temporary file in the same folder as courses.json.
        # Using the same folder makes os.replace work reliably.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=DATA_FILE.parent,
            suffix=".json"
        ) as temp_file:
            temp_file_name = temp_file.name
            json.dump(courses, temp_file, indent=2)

        # Replace the old file with the new complete file.
        os.replace(temp_file_name, DATA_FILE)

        return True, None

    except (OSError, TypeError) as error:
        # Remove the temporary file if something went wrong.
        if temp_file_name and os.path.exists(temp_file_name):
            os.remove(temp_file_name)

        return False, f"Unable to write courses.json: {error}"


def find_course_by_id(courses, course_id):
    """
    Find one course in a list by its ID.

    Returns:
        The course dictionary if found, otherwise None.
    """
    for course in courses:
        if course.get("id") == course_id:
            return course

    return None


def get_next_id(courses):
    """
    Generate the next course ID.

    IDs start at 1. If courses already exist, the new ID will be
    one larger than the highest existing ID.
    """
    if not courses:
        return 1

    highest_id = max(course.get("id", 0) for course in courses)
    return highest_id + 1


def is_valid_date(date_string):
    """
    Check that a target date uses the exact YYYY-MM-DD format
    and is a real calendar date.
    """
    if not isinstance(date_string, str):
        return False

    # Require leading zeroes, such as 2026-01-05.
    if not DATE_PATTERN.match(date_string):
        return False

    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_course_data(data):
    """
    Validate the fields required to create or fully update a course.

    Expected fields:
        - name
        - description
        - target_date
        - status

    Returns:
        An error message string if validation fails.
        None if validation succeeds.
    """
    required_fields = ["name", "description", "target_date", "status"]

    # Check for missing fields.
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] is None
    ]

    if missing_fields:
        return f"Missing required field(s): {', '.join(missing_fields)}"

    # Validate name.
    if not isinstance(data["name"], str) or not data["name"].strip():
        return "Name must be a non-empty string."

    # Validate description.
    if not isinstance(data["description"], str) or not data["description"].strip():
        return "Description must be a non-empty string."

    # Validate target date.
    if not is_valid_date(data["target_date"]):
        return "target_date must be a valid date in YYYY-MM-DD format."

    # Validate status.
    if data["status"] not in VALID_STATUSES:
        return (
            "Invalid status. Status must be one of: "
            + ", ".join(VALID_STATUSES)
        )

    return None


@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Create a new course.

    Endpoint:
        POST /api/courses
    """
    # silent=True avoids Flask raising its own error for invalid JSON.
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    courses, read_error = read_courses()

    if read_error:
        return jsonify({"error": read_error}), 500

    # Create the new course object.
    new_course = {
        "id": get_next_id(courses),
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    courses.append(new_course)

    success, write_error = write_courses(courses)

    if not success:
        return jsonify({"error": write_error}), 500

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """
    Get all courses.

    Endpoint:
        GET /api/courses
    """
    courses, read_error = read_courses()

    if read_error:
        return jsonify({"error": read_error}), 500

    return jsonify(courses), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    Get one course by ID.

    Endpoint:
        GET /api/courses/<course_id>

    Example:
        GET /api/courses/1
    """
    courses, read_error = read_courses()

    if read_error:
        return jsonify({"error": read_error}), 500

    course = find_course_by_id(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Fully update an existing course.

    Endpoint:
        PUT /api/courses/<course_id>

    The request body must include:
        - name
        - description
        - target_date
        - status

    The course ID and created_at timestamp cannot be changed.
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    courses, read_error = read_courses()

    if read_error:
        return jsonify({"error": read_error}), 500

    course = find_course_by_id(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    # Update only fields that are allowed to change.
    course["name"] = data["name"].strip()
    course["description"] = data["description"].strip()
    course["target_date"] = data["target_date"]
    course["status"] = data["status"]

    success, write_error = write_courses(courses)

    if not success:
        return jsonify({"error": write_error}), 500

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete a course by ID.

    Endpoint:
        DELETE /api/courses/<course_id>

    Example:
        DELETE /api/courses/1
    """
    courses, read_error = read_courses()

    if read_error:
        return jsonify({"error": read_error}), 500

    course = find_course_by_id(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    courses.remove(course)

    success, write_error = write_courses(courses)

    if not success:
        return jsonify({"error": write_error}), 500

    return jsonify({
        "message": f"Course with ID {course_id} was deleted successfully."
    }), 200


if __name__ == "__main__":
    # Create courses.json automatically before starting the server.
    ensure_data_file_exists()

    # debug=True automatically restarts the server when code changes.
    # Do not use debug=True in production.
    app.run(debug=True)