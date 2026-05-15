# ProtoApp - Production Ready Project

This document provides a summary of **ProtoApp**, a production-ready FastAPI application. This project demonstrates advanced features such as database integration with SQLAlchemy 2.0, sophisticated logging configurations, custom middleware, load testing, and comprehensive testing strategies including coverage analysis.

## Project Structure

The project is organized into a modular structure to ensure maintainability and scalability:

- `protoapp/main.py`: The entry point of the FastAPI application. It includes endpoint definitions, dependency injection for database sessions, and custom middleware.
- `protoapp/database.py`: Handles database connectivity and ORM models using the modern SQLAlchemy 2.0 syntax.
- `protoapp/logging.py`: Configures advanced logging, including colorized console output and timed rotating file logs.
- `run_server.py`: A utility script to launch the Uvicorn server with auto-reload and debugging support.
- `locustfile.py`: Defines tasks for load testing the application using the Locust framework.
- `tests/conftest.py`: Contains shared pytest fixtures, such as the test database engine and the test client with dependency overrides.
- `tests/test_main.py`: Includes unit and integration tests, demonstrating both synchronous and asynchronous testing patterns.
- `pytest.ini`: Configuration file for pytest, defining python path and custom test markers.

## Features

### 1. Modern Database Integration (SQLAlchemy 2.0)

- **File:** `protoapp/database.py`, `protoapp/main.py`
- **Description:** The project uses SQLAlchemy 2.0's `DeclarativeBase` and type-hinted `Mapped` columns for a more robust and Pythonic ORM layer. It implements a session management pattern using a generator dependency (`get_db_session`) to ensure proper resource cleanup.

### 2. Advanced Logging Configuration

- **File:** `protoapp/logging.py`
- **Description:** Implements a dual-handler logging system:
    - **Console Handler:** Uses `ColourizedFormatter` (from Uvicorn) to provide readable, color-coded logs in the terminal.
    - **File Handler:** Uses `TimedRotatingFileHandler` to store logs in `app.log`, automatically rotating the files based on time to manage disk space.

### 3. Custom HTTP Middleware

- **File:** `protoapp/main.py`
- **Description:** A custom "http" middleware (`log_requests`) captures details of every incoming request (method, path, and client IP) and logs them using the application's logger before passing the request to the next handler.

### 4. Load Testing with Locust

- **File:** `locustfile.py`
- **Description:** Provides a performance testing suite that simulates multiple concurrent users. It allows developers to monitor how the application handles traffic spikes and identify potential bottlenecks via a web interface or headless mode.

### 5. Comprehensive Testing Suite

- **File:** `tests/test_main.py`, `tests/conftest.py`
- **Description:** 
    - **Unit & Integration Tests:** Covers everything from simple endpoint checks to full database round-trips.
    - **Async Testing:** Uses `httpx.AsyncClient` to test asynchronous endpoints properly.
    - **Dependency Overrides:** Demonstrates how to swap the production database for an in-memory SQLite database during tests for isolation and speed.
    - **Custom Markers:** Uses `pytest.mark.integration` to separate different types of tests.

### 6. Test Coverage and Reporting

- **Tools:** `pytest-cov`, `coverage`
- **Description:** The project is set up to measure code coverage. Running `pytest --cov protoapp tests` generates a `.coverage` file, which can then be used to create a detailed HTML report (`coverage html`) to visualize which parts of the code are exercised by tests.

## Advanced Python Features Used

- **Type Hinting:** Extensive use of Python type hints for better IDE support and runtime validation via Pydantic and SQLAlchemy.
- **Asynchronous Programming:** Leverages `async/await` for middleware and testing, maximizing the performance benefits of FastAPI.
- **Generators:** Uses the `yield` keyword in dependencies for clean resource management (Context Managers).
- **Decorators:** Utilizes FastAPI and Pytest decorators to define routes, middleware, and test metadata.
- **Markers:** Implements custom Pytest markers for granular test execution control.

---

### How to Run

1. **Start the server:**
   ```bash
   python run_server.py
   ```

2. **Run Tests:**
   ```bash
   pytest
   ```

3. **Run Load Tests:**
   ```bash
   locust
   ```
