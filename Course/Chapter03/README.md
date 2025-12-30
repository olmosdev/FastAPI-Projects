# Task Manager API

This project is a simple but powerful Task Management API built with FastAPI. It demonstrates several key features of modern Python web development, from basic RESTful principles to more advanced concepts like authentication, testing, and API documentation customization.

## How to Run the Application

To run the API server, you need `uvicorn`. From the `task_manager_app` directory, run:

```bash
uvicorn main:app --reload
```

This will start a local development server.

## Features

- **RESTful API Endpoints**: Full CRUD (Create, Read, Update, Delete) operations for tasks.
- **CSV Database**: Uses a simple `tasks.csv` file as a database, showcasing how to work with files.
- **API Versioning**: Includes a simple `v2` endpoint to show how an API can evolve.
- **Authentication**: A basic OAuth2-like password flow to secure certain endpoints.
- **Comprehensive Testing**: Uses `pytest` to test both the API endpoints and the underlying business logic.
- **Custom OpenAPI Schema**: Modifies the default OpenAPI (Swagger UI) documentation.

---

## Technical Deep Dive

This section explains the key concepts used in the project in simple terms.

### 1. RESTful API with FastAPI

A RESTful API is an architectural style for providing standards between computer systems on the web, making it easier for systems to communicate with each other. This project uses FastAPI to create RESTful endpoints.

- **`@app.get("/tasks")`**: Defines a `GET` endpoint to list all tasks.
- **`@app.post("/task")`**: Defines a `POST` endpoint to create a new task.
- **`@app.put("/task/{task_id}")`**: Defines a `PUT` endpoint to update a task by its ID.
- **`@app.delete("/task/{task_id}")`**: Defines a `DELETE` endpoint to remove a task by its ID.

FastAPI uses Python type hints, which helps to automatically validate incoming data and serialize outgoing data.

### 2. Pydantic for Data Validation

Pydantic models are used to define the shape of the data. FastAPI uses these models to validate request data and format response data.

In `models.py`, you can see classes like `Task` and `TaskWithID`.

```python
class Task(BaseModel):
    title: str
    description: str
    status: str
```

When a client sends data to create a task, FastAPI validates that the data has a `title`, `description`, and `status`, and that they are all strings.

### 3. Data Storage with CSV

The project uses a standard CSV (Comma-Separated Values) file (`tasks.csv`) for data storage. The `operations.py` file contains all the functions that interact with this file. It uses Python's built-in `csv` module to read from and write to the database file.

This approach is simple and doesn't require an external database server, making it great for small projects or prototypes.

### 4. API Versioning

The API includes a second version of the "get tasks" endpoint, located at `/v2/tasks`. This endpoint returns a `TaskV2WithID` model, which includes an extra `priority` field. This is a common strategy to add new features to an API without breaking existing client integrations.

### 5. Authentication with OAuth2 Password Flow

The project implements a basic user authentication system in `security.py`.

- **How it works**: A client can send a `username` and `password` to the `/token` endpoint. If the credentials are correct, the server returns an "access token".
- **`OAuth2PasswordBearer`**: This is a FastAPI utility that helps manage the token flow.
- **Protected Endpoints**: Endpoints that require authentication use `Depends(get_user_from_token)`. This tells FastAPI to run the security check before executing the main logic. If the token is invalid or missing, it returns a 401 "Unauthorized" error.
- **Note**: The implementation uses a fake in-memory user database and a simple token generation scheme. It is **not secure** and is for demonstration purposes only.

### 6. Comprehensive Testing with `pytest`

Testing is a critical part of software development. This project has a good test suite that covers both the API endpoints and the internal logic.

- **`TestClient`**: FastAPI's `TestClient` (`test_main.py`) allows you to make requests to your API directly in your tests without needing a running server. This makes tests fast and reliable.
- **Fixtures (`conftest.py`)**: The tests use a `pytest` fixture to create a temporary, clean database (`test_tasks.csv`) for each test function. This ensures that tests are isolated and don't interfere with each other.
- **Mocking**: The fixture uses `unittest.mock.patch` to temporarily redirect the application's database file path to the test database. This is a powerful technique for controlling the environment during tests.

### 7. OpenAPI (Swagger) Customization

FastAPI automatically generates interactive API documentation (using Swagger UI) that you can see at `/docs`. This project includes a function (`custom_openapi` in `main.py`) to customize this documentation. In this case, it is used to hide the `/token` endpoint from the public API documentation, as it's a utility endpoint that clients don't need to see in the main list.
