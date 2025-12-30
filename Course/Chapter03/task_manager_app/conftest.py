import csv
import os
from pathlib import Path
from unittest.mock import patch

import pytest

TEST_DATABASE_FILE = "test_tasks.csv"

# Define the initial raw data for the CSV file.
# Note that all values, including 'id', are strings because CSV files store data as text.
TEST_TASKS_CSV = [
    {
        "id": "1",
        "title": "Test Task One",
        "description": "Test Description One",
        "status": "Incomplete",
    },
    {
        "id": "2",
        "title": "Test Task Two",
        "description": "Test Description Two",
        "status": "Ongoing",
    },
]

# Create a processed list of tasks where 'id' is converted to an integer.
# This is useful for asserting equality against API responses which usually return integer IDs.
TEST_TASKS = [
    {**task_json, "id": int(task_json["id"])}
    for task_json in TEST_TASKS_CSV
]

# This pytest fixture handles the setup and teardown for tests.
# 'autouse=True' ensures it runs automatically before every test function in this scope, guaranteeing a clean state.
@pytest.fixture(autouse=True)
def create_test_database():
    # Construct the absolute path for the temporary 'test_tasks.csv' file relative to this script's location.
    # This ensures the path is correct regardless of where the test command is run from.
    database_file_location = str(
        Path(__file__).parent / TEST_DATABASE_FILE
    )
    # Use 'unittest.mock.patch' to temporarily replace the 'DATABASE_FILENAME' variable in the 'operations' module.
    # This redirects all database operations to our temporary test file instead of the real production database.
    with patch(
        "operations.DATABASE_FILENAME",
        database_file_location,
    ) as csv_test:
        # Open the temporary file in write mode ('w') to initialize the database.
        # 'newline=""' is required by the csv module to prevent extra blank lines on Windows.
        with open(
            database_file_location, mode="w", newline=""
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "id",
                    "title",
                    "description",
                    "status",
                ],
            )
            writer.writeheader()
            writer.writerows(TEST_TASKS_CSV)
            print("")
        # The 'yield' statement pauses the fixture execution and allows the test function to run.
        # The object yielded (csv_test) is available to the test function if needed.
        yield csv_test
        # Teardown phase: This code runs after the test finishes (whether it passed or failed).
        # We remove the temporary CSV file to ensure no side effects persist for subsequent tests.
        os.remove(database_file_location)
