# Chapter 01: FastAPI Fundamentals

This chapter covers the basics of creating a FastAPI application, from a simple "Hello World" to a more structured project with data validation and error handling.

## bookstore

This subproject demonstrates a simple Book API.

-   **What it does:** It provides endpoints to get books by ID, list all books, and create new books. It simulates a book database using in-memory data.
-   **Key Features:**
    -   **Pydantic Models (`models.py`):** Uses `pydantic.BaseModel` for robust data validation. The `Book` model defines the expected data types, and `Field` is used to add constraints like `min_length`, `max_length`, and value ranges (`gt`, `lt`). This ensures data integrity for incoming requests.
    -   **Path and Query Parameters:** Shows the use of path parameters (e.g., `/books/{book_id}`) to identify specific resources and query parameters (e.g., `/books?year=2010`) for filtering.
    -   **Response Model:** The `/allbooks` endpoint uses a `response_model` (`list[BookResponse]`) to define the exact schema of the output, ensuring the API's response is consistent and automatically filtering out extra data.
    -   **Custom Exception Handlers:** Implements custom handlers for `HTTPException` and `RequestValidationError`. This is an advanced feature that allows for centralized and consistent error responses across the application, rather than using default FastAPI error messages.

## fastapi_start

This subproject shows a minimal FastAPI application and introduces code organization with `APIRouter`.

-   **What it does:** It creates a basic root endpoint (`/`) and another endpoint (`/items/{item_id}`) in a separate file.
-   **Key Features:**
    -   **`APIRouter`:** This is a key feature for organizing larger applications. By creating an `APIRouter` instance in `router_example.py`, endpoints can be defined in a separate module ("router").
    -   **`app.include_router()`:** The main application in `main.py` uses `app.include_router()` to incorporate the endpoints from the external router. This makes the codebase modular, scalable, and easier to maintain.
