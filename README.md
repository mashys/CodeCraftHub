# CodeCraftHub

CodeCraftHub is a simple beginner-friendly REST API built with **Python** and **Flask**.

It allows developers to track courses they want to learn. You can create, view, update, and delete courses using HTTP requests.

This project uses a JSON file named `courses.json` to store data instead of a database. It is designed to help beginners understand REST API concepts such as:

- HTTP methods (`GET`, `POST`, `PUT`, `DELETE`)
- Request URLs and route parameters
- JSON request and response data
- HTTP status codes
- Input validation
- Basic file-based data storage

---

## Features

- Create a new learning course
- View all courses
- View a single course by ID
- Update a course
- Delete a course
- Automatically generate course IDs
- Automatically create the `courses.json` data file
- Store data in a local JSON file
- Validate required fields
- Validate course status values
- Validate dates in `YYYY-MM-DD` format
- Return helpful error messages
- No database required
- No authentication or user accounts required

---

## Technologies Used

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- JSON file storage
- `curl` for testing API endpoints

---

## Project Structure

Your project folder should look like this:

```text
codecrafthub/
├── app.py
├── courses.json
├── requirements.txt
└── README.md
```

### Files Explained

| File | Purpose |
| --- | --- |
| `app.py` | The main Flask application. It contains the API routes, validation, JSON file functions, and error handling. |
| `courses.json` | Stores course data as JSON. The application creates this file automatically if it does not exist. |
| `requirements.txt` | Lists Python packages needed by the project. |
| `README.md` | Project documentation and setup instructions. |

### Course Data Format

Each course contains the following fields:

| Field | Description | Example |
| --- | --- | --- |
| `id` | Auto-generated numeric course ID | `1` |
| `name` | Course name | `"Flask REST API Basics"` |
| `description` | Description of the course | `"Learn how to build APIs with Flask."` |
| `target_date` | Target completion date | `"2026-12-31"` |
| `status` | Learning progress status | `"Not Started"` |
| `created_at` | Auto-generated creation timestamp | `"2026-09-23T12:00:00+00:00"` |

Valid status values are:

- Not Started
- In Progress
- Completed

Example course object:

```json
{
  "id": 1,
  "name": "Flask REST API Basics",
  "description": "Learn how to build REST APIs using Python and Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-09-23T12:00:00+00:00"
}
```

---

## Installation

Follow these steps to install and run CodeCraftHub.

### 1. Install Python

Make sure Python 3 is installed on your computer.

Check your Python version:

```bash
python --version
```

If that does not work, try:

```bash
python3 --version
```

You should see a version similar to:

```text
Python 3.10.0
```

Download Python from:

https://www.python.org/downloads/

### 2. Create a Project Folder

Open your terminal and create a new folder:

```bash
mkdir codecrafthub
```

Move into the folder:

```bash
cd codecrafthub
```

### 3. Create a Virtual Environment

A virtual environment keeps this project's packages separate from other Python projects.

Create it:

```bash
python -m venv venv
```

If your system uses `python3`:

```bash
python3 -m venv venv
```

Activate the virtual environment.

- Windows Command Prompt:

```bash
venv\Scripts\activate
```

- Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

- macOS or Linux:

```bash
source venv/bin/activate
```

When activated, your terminal usually shows `(venv)` at the beginning of the line.

Example:

```text
(venv) user@computer:~/codecrafthub$
```

### 4. Create `requirements.txt`

Create a file named `requirements.txt` and add:

```text
Flask==3.0.3
```

You can also install the latest Flask version by using:

```text
Flask
```

### 5. Install Flask

Run:

```bash
pip install -r requirements.txt
```

Or install Flask directly:

```bash
pip install Flask
```

Check that Flask was installed:

```bash
pip show Flask
```

### 6. Add the Application Code

Create a file named `app.py`.

Copy the CodeCraftHub Flask application code into `app.py`.

You do not need to manually create `courses.json`. The application automatically creates it when you start the server.

If you do create it manually, its contents should be:

```json
[]
```

---

## Running the Application

Start the Flask application with:

```bash
python app.py
```

If your computer uses `python3`, run:

```bash
python3 app.py
```

You should see output similar to this:

```text
* Running on http://127.0.0.1:5000
* Debug mode: on
```

Your API is now available at:

```text
http://127.0.0.1:5000
```

To stop the server, press:

```text
Ctrl + C
```

---

## REST API Basics

A REST API uses HTTP methods to perform actions on resources.

In CodeCraftHub, the resource is a course.

| HTTP Method | Meaning | CodeCraftHub Example |
| --- | --- | --- |
| `GET` | Read data | Get all courses |
| `POST` | Create new data | Create a course |
| `PUT` | Fully update existing data | Update a course |
| `DELETE` | Remove data | Delete a course |

The API base URL is:

```text
http://127.0.0.1:5000
```

All course endpoints begin with:

```text
/api/courses
```

---

## API Endpoints

### 1. Create a Course

Creates a new course.

**Request**

```text
POST /api/courses
```

**URL**

```text
http://127.0.0.1:5000/api/courses
```

**Required Request Body**

```json
{
  "name": "Flask REST API Basics",
  "description": "Learn how to build REST APIs using Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

**Valid Status Values**

- Not Started
- In Progress
- Completed

**Example `curl` command**

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST API Basics",
    "description": "Learn how to build REST APIs using Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
```

**Successful Response**

**Status:** `201 Created`

```json
{
  "created_at": "2026-09-23T12:00:00+00:00",
  "description": "Learn how to build REST APIs using Flask.",
  "id": 1,
  "name": "Flask REST API Basics",
  "status": "Not Started",
  "target_date": "2026-12-31"
}
```

The `id` and `created_at` values are generated automatically.

### 2. Get All Courses

Returns every course stored in `courses.json`.

**Request**

```text
GET /api/courses
```

**URL**

```text
http://127.0.0.1:5000/api/courses
```

**Example `curl` command**

```bash
curl -i http://127.0.0.1:5000/api/courses
```

**Successful Response**

**Status:** `200 OK`

```json
[
  {
    "created_at": "2026-09-23T12:00:00+00:00",
    "description": "Learn how to build REST APIs using Flask.",
    "id": 1,
    "name": "Flask REST API Basics",
    "status": "Not Started",
    "target_date": "2026-12-31"
  }
]
```

If there are no courses, the API returns:

```json
[]
```

### 3. Get a Course by ID

Returns one course using its ID.

**Request**

```text
GET /api/courses/<course_id>
```

**Example URL**

```text
http://127.0.0.1:5000/api/courses/1
```

**Example `curl` command**

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

**Successful Response**

**Status:** `200 OK`

```json
{
  "created_at": "2026-09-23T12:00:00+00:00",
  "description": "Learn how to build REST APIs using Flask.",
  "id": 1,
  "name": "Flask REST API Basics",
  "status": "Not Started",
  "target_date": "2026-12-31"
}
```

**Course Not Found Response**

**Status:** `404 Not Found`

```json
{
  "error": "Course with ID 999 was not found."
}
```

### 4. Update a Course

Updates all editable fields for an existing course.

**Request**

```text
PUT /api/courses/<course_id>
```

A `PUT` request requires all editable fields: `name`, `description`, `target_date`, and `status`.

**Example URL**

```text
http://127.0.0.1:5000/api/courses/1
```

**Required Request Body**

```json
{
  "name": "Flask REST API Fundamentals",
  "description": "Build and test REST APIs using Flask.",
  "target_date": "2026-12-20",
  "status": "In Progress"
}
```

**Example `curl` command**

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST API Fundamentals",
    "description": "Build and test REST APIs using Flask.",
    "target_date": "2026-12-20",
    "status": "In Progress"
  }'
```

**Successful Response**

**Status:** `200 OK`

```json
{
  "created_at": "2026-09-23T12:00:00+00:00",
  "description": "Build and test REST APIs using Flask.",
  "id": 1,
  "name": "Flask REST API Fundamentals",
  "status": "In Progress",
  "target_date": "2026-12-20"
}
```

The `id` and `created_at` fields do not change when a course is updated.

### 5. Delete a Course

Deletes a course using its ID.

**Request**

```text
DELETE /api/courses/<course_id>
```

**Example URL**

```text
http://127.0.0.1:5000/api/courses/1
```

**Example `curl` command**

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

**Successful Response**

**Status:** `200 OK`

```json
{
  "message": "Course with ID 1 was deleted successfully."
}
```

**Course Not Found Response**

**Status:** `404 Not Found`

```json
{
  "error": "Course with ID 999 was not found."
}
```

---

## HTTP Status Codes Used

| Status Code | Name | Meaning |
| --- | --- | --- |
| `200` | `OK` | The request completed successfully. |
| `201` | `Created` | A new course was created successfully. |
| `400` | `Bad Request` | The JSON body or course data is invalid. |
| `404` | `Not Found` | The requested course ID does not exist. |
| `500` | `Internal Server Error` | The API could not read or write `courses.json`. |

---

## Validation and Error Examples

### Missing Required Fields

Example request with only a course name:

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course"
  }'
```

Expected response:

```http
HTTP/1.1 400 BAD REQUEST
{
  "error": "Missing required field(s): description, target_date, status"
}
```

### Invalid Status

The following request uses an invalid status value:

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Course",
    "description": "Testing invalid status validation.",
    "target_date": "2026-12-31",
    "status": "Paused"
  }'
```

Expected response:

```http
HTTP/1.1 400 BAD REQUEST
{
  "error": "Invalid status. Status must be one of: Not Started, In Progress, Completed"
}
```

### Invalid Date Format

Dates must use this format: `YYYY-MM-DD`.

Correct:

```text
2026-12-31
```

Incorrect:

```text
12/31/2026
```

Test invalid date formatting:

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Date Test Course",
    "description": "Testing an invalid date format.",
    "target_date": "12/31/2026",
    "status": "Not Started"
  }'
```

Expected response:

```http
HTTP/1.1 400 BAD REQUEST
{
  "error": "target_date must be a valid date in YYYY-MM-DD format."
}
```

---

## Testing the API

You can test this API with:

- `curl`
- Postman
- Insomnia
- VS Code REST Client extension
- Thunder Client extension for VS Code

For beginners, `curl` is a good starting point because it is available in many terminals.

### Basic CRUD Test Sequence

Before testing, you can reset your data file.

Stop the server, then set `courses.json` to:

```json
[]
```

Start the server again:

```bash
python app.py
```

#### Step 1: Get All Courses

```bash
curl -i http://127.0.0.1:5000/api/courses
```

Expected response:

```json
[]
```

#### Step 2: Create a Course

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Learn Flask",
    "description": "Build a beginner REST API with Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
```

Expected result:

```text
HTTP/1.1 201 CREATED
```

#### Step 3: Read the Course

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

Expected result:

```text
HTTP/1.1 200 OK
```

#### Step 4: Update the Course

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Learn Flask REST APIs",
    "description": "Build and test a beginner REST API with Flask.",
    "target_date": "2026-12-15",
    "status": "In Progress"
  }'
```

Expected result:

```text
HTTP/1.1 200 OK
```

#### Step 5: Delete the Course

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

Expected result:

```text
HTTP/1.1 200 OK
```

#### Step 6: Confirm the Course Was Deleted

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

Expected result:

```text
HTTP/1.1 404 NOT FOUND
```

---

## Troubleshooting

### `python` Command Is Not Found

Try using:

```bash
python3 app.py
```

Also check whether Python is installed:

```bash
python --version
```

or:

```bash
python3 --version
```

If Python is not installed, download it from:

https://www.python.org/downloads/

On Windows, make sure you select **Add Python to PATH** during installation.

### `ModuleNotFoundError: No module named 'flask'`

Flask is not installed in your current Python environment.

Activate your virtual environment, then install Flask:

```bash
pip install Flask
```

Or use:

```bash
pip install -r requirements.txt
```

To confirm Flask is installed:

```bash
pip show Flask
```

### Virtual Environment Will Not Activate on Windows PowerShell

PowerShell may block script execution.

You can either use Command Prompt instead:

```bash
venv\Scripts\activate
```

Or, if appropriate for your development computer, allow scripts for the current terminal session:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then activate again:

```powershell
venv\Scripts\Activate.ps1
```

### Address already in use / Port 5000 is in use

Another application is already using Flask's default port.

Stop other Flask servers by pressing:

```text
Ctrl + C
```

Or change the port in `app.py`:

```python
app.run(debug=True, port=5001)
```

Then use:

```text
http://127.0.0.1:5001
```

instead of port `5000`.

### `courses.json` contains invalid JSON

This means the contents of `courses.json` are not valid JSON.

For a clean starting point, stop the server and replace the file contents with:

```json
[]
```

Remember:

- JSON uses double quotes, not single quotes.
- Do not add a comma after the last item in a list.
- Do not add comments inside JSON files.

Valid example:

```json
[
  {
    "id": 1,
    "name": "Flask Basics"
  }
]
```

Invalid example:

```json
[
  {
    "id": 1,
    "name": "Flask Basics",
  }
]
```

The comma after `"Flask Basics"` makes the second example invalid.

### API Returns `404 Not Found`

Check the URL carefully.

Correct examples:

```text
GET http://127.0.0.1:5000/api/courses
GET http://127.0.0.1:5000/api/courses/1
```

Also make sure the Flask application is running in a terminal.

### API Returns `400 Bad Request`

A `400` response usually means the request body is missing required fields or contains invalid data.

Check that your JSON includes all required fields:

```json
{
  "name": "Course Name",
  "description": "Course description",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
```

Check that:

- `name` is not empty.
- `description` is not empty.
- `target_date` uses `YYYY-MM-DD`.
- `status` is exactly `Not Started`, `In Progress`, or `Completed`.

JSON keys and text values use double quotes.

### Changes Do Not Appear in `courses.json`

Make sure you are viewing the `courses.json` file in the same folder where you run:

```bash
python app.py
```

You can check your current directory:

- macOS/Linux:

```bash
pwd
```

- Windows:

```bash
cd
```

You should run the server from inside the CodeCraftHub project directory.

### `curl` Does Not Work on Windows

Modern Windows usually includes `curl`. Check by running:

```bash
curl --version
```

If needed, you can use another API client such as:

- Postman
- Insomnia
- Thunder Client for VS Code
- VS Code REST Client extension

---

## Learning Notes

### What Is JSON?

JSON stands for JavaScript Object Notation. It is a common text format used to send and store data.

Example JSON object:

```json
{
  "name": "Learn Flask",
  "status": "In Progress"
}
```

Example JSON list:

```json
[
  {
    "id": 1,
    "name": "Learn Flask"
  },
  {
    "id": 2,
    "name": "Learn Python"
  }
]
```

### What Is an API Endpoint?

An endpoint is a URL where an API receives requests.

For example:

```text
http://127.0.0.1:5000/api/courses
```

This endpoint represents the collection of all courses.

```text
http://127.0.0.1:5000/api/courses/1
```

This endpoint represents one specific course with ID `1`.

### Why Use a JSON File Instead of a Database?

Using a JSON file makes this project easier to understand because no database setup is required.

This approach is suitable for:

- Learning projects
- Small prototypes
- Personal experiments

It is not suitable for production applications with many users because a JSON file can have problems with simultaneous writes, searching, backups, and scaling.

When you are ready, you can upgrade CodeCraftHub to use:

- SQLite
- PostgreSQL
- MySQL
- MongoDB

---

## Future Improvements

Once you understand the current API, you could add:

- `PATCH /api/courses/<id>` for partial updates
- Filtering courses by status
- Sorting by target date
- Search by course name
- A frontend interface with HTML, CSS, and JavaScript
- A React or Vue frontend
- User accounts and authentication
- SQLite or PostgreSQL storage
- Automated tests using `pytest`
- API documentation using Swagger/OpenAPI
- Docker support
- Deployment to Render, Railway, or PythonAnywhere

---

## License

This project is intended for learning and practice. You may modify and reuse it for personal or educational projects.
