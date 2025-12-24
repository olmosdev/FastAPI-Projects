# Import the time module to handle time-related operations and timestamps
import time
# Import asyncio module for asynchronous programming capabilities
import asyncio
# Import contextmanager decorator to create reusable context managers
from contextlib import contextmanager
# Import Process class from multiprocessing to run server in a separate process
from multiprocessing import Process

# Import uvicorn to run the ASGI server application
import uvicorn
# Import AsyncClient from httpx for making asynchronous HTTP requests
from httpx import AsyncClient

# Import the FastAPI application instance from the main module
from main import app

# Define a function that runs the uvicorn server
def run_server():
    # Start the FastAPI app on port 8000 with error-level logging only
    uvicorn.run(app, port=8000, log_level="error")

# Define a context manager to manage the server process lifecycle
@contextmanager
def run_server_in_process():
    # Create a Process object that will run the run_server function
    p = Process(target=run_server)
    # Start the process execution in the background
    p.start()
    # Pause for 2 seconds to allow the server time to initialize and start listening
    time.sleep(2) # Give the server a second to start
    # Print a confirmation message that the server is running
    print("Server is running in a separate process.")
    # Yield control back to the caller so they can use the running server
    yield
    # Terminate the server process when exiting the context manager
    p.terminate()

# Define an async function that makes multiple concurrent HTTP requests to an endpoint
async def make_requests_to_the_endpoint(n: int, path: str):
    # Create an async HTTP client context with the base URL pointing to the local server
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # Create a generator expression that builds n concurrent GET requests to the specified path
        tasks = (
            # Make a GET request with infinite timeout to avoid premature request cancellation
            client.get(path, timeout=float("inf"))
            # Generate a request for each iteration up to n times
            for _ in range(n)
        )

        # Execute all tasks concurrently and wait for all of them to complete
        await asyncio.gather(*tasks)

# Define the main async function that orchestrates the performance testing (default 10 requests)
async def main(n: int = 10):
    # Use the server context manager to start the server process
    with run_server_in_process():
        # Record the current time before making sync endpoint requests
        begin = time.time()
        # Make n asynchronous requests to the synchronous endpoint and wait for them to complete
        await make_requests_to_the_endpoint(n, "/sync")
        # Record the current time after all requests to sync endpoint finish
        end = time.time()
        # Print the elapsed time for the synchronous endpoint requests
        print(
            f"Time taken to make {n} request "
            f"to async endpoint: {end - begin} seconds"
        )

        # Record the current time before making async endpoint requests
        begin = time.time()
        # Make n asynchronous requests to the async endpoint and wait for them to complete
        await make_requests_to_the_endpoint(n, "/async")
        # Record the current time after all requests to async endpoint finish
        end = time.time()
        # Print the elapsed time for the asynchronous endpoint requests
        print(
            f"Time taken to make {n} requests "
            f"to async endpoint: {end - begin} seconds"
        )

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Run the main async function with 100 concurrent requests using asyncio event loop
    asyncio.run(main(n=100))
