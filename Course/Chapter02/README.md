# Chapter 02: Advanced FastAPI Features

This chapter explores more advanced FastAPI concepts, including asynchronous programming, database integrations with both SQL and NoSQL databases, and handling file I/O.

## async_example

This subproject provides a clear, side-by-side comparison of synchronous and asynchronous endpoint execution.

-   **What it does:** It contains two endpoints, `/sync` and `/async`. Both use a 2-second delay to simulate a long-running task.
-   **Key Features:**
    -   **Synchronous Blocking (`/sync`):** Uses Python's standard `time.sleep(2)`. When this endpoint is called, it blocks the entire server process. Multiple simultaneous requests will be handled one after another.
    -   **Asynchronous Non-Blocking (`/async`):** Uses `async def` and `await asyncio.sleep(2)`. This is a core feature of FastAPI. It allows the server to handle other requests while waiting for the "sleep" to complete, leading to much higher performance and concurrency for I/O-bound tasks.

## sql_example

This project demonstrates how to integrate a SQL database (SQLite) with a FastAPI application using SQLAlchemy as the ORM.

-   **What it does:** It provides a full set of CRUD (Create, Read, Update, Delete) API endpoints to manage a `users` table in a SQLite database.
-   **Key Features:**
    -   **SQLAlchemy ORM (`database.py`):** Defines a `User` model that maps to a database table using SQLAlchemy's `DeclarativeBase`. This allows developers to interact with the database using Python objects instead of raw SQL queries.
    -   **Dependency Injection (`Depends`):** The `get_db` function is a generator that yields a database session. By using `db: Session = Depends(get_db)` in the endpoint function signatures, FastAPI ensures that a new session is created for each request and properly closed afterward, even if errors occur. This is a robust pattern for managing resources like database connections.
    -   **CRUD Operations:** The endpoints show best practices for creating, querying, updating, and deleting records using the SQLAlchemy session.

## nosql_example

This project shows how to connect a FastAPI application to a NoSQL database, specifically MongoDB.

-   **What it does:** It offers endpoints to create and retrieve users from a MongoDB collection.
-   **Key Features:**
    -   **MongoDB Integration (`database.py`):** Uses the `pymongo` library to establish a connection to a MongoDB server and get a handle on a specific database and collection.
    -   **Pydantic with Nested Models:** The `User` model contains a nested `Tweet` model, demonstrating how Pydantic can validate complex, nested JSON objects.
    -   **Custom Field Validators (`@field_validator`):** The `User` model includes a custom validator for the `age` field. This Pydantic feature allows for complex validation logic beyond simple type checking.
    -   **BSON `ObjectId` Handling:** The code correctly handles MongoDB's `ObjectId` type, converting it to and from strings for use in the API, which is a necessary step when bridging the gap between JSON and BSON.

## uploads_downloads

This subproject demonstrates how to manage file uploads and downloads.

-   **What it does:** It provides one endpoint to upload a file to the server and another to download it.
-   **Key Features:**
    -   **`UploadFile`:** The `/uploadfile` endpoint uses `UploadFile` as a type hint. This is a key FastAPI feature that handles streaming the incoming file data efficiently, preventing memory overload with large files. The file is then saved to the local `uploads/` directory.
    -   **`FileResponse`:** The `/downloadfile/{filename}` endpoint uses `FileResponse` to serve a file directly from the filesystem. FastAPI automatically sets the appropriate `Content-Disposition` and `Content-Type` headers, allowing the browser to correctly handle the file download.
