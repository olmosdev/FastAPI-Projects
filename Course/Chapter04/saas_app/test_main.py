import pytest
from fastapi.testclient import TestClient

from db_connection import get_session
from main import app


# Fixture to create a TestClient for the FastAPI app.
# It receives the 'session' fixture (from conftest.py) which is connected to the in-memory test database.
@pytest.fixture
def client(session):
    # Dependency Override:
    # We replace the 'get_session' dependency used in the main app with the test 'session'.
    # This ensures that when the app runs this test, it uses the in-memory database instead of the real one.
    # The '|=' operator (in-place union) updates the dictionary with new key-value pairs.
    # It is equivalent to 'app.dependency_overrides.update({...})'.
    # This ensures we don't overwrite existing overrides if any were set previously.
    app.dependency_overrides |= {
        get_session: lambda: session
    }
    
    # Create the TestClient, which allows making HTTP requests to the app without running a server.
    testclient = TestClient(app)
    return testclient


def test_endpoint_add_basic_user(client):
    # Define the payload for a new user.
    user = {
        "username": "lyampayet",
        "password": "difficultpassword",
        "email": "lyampayet@email.com",
    }

    # Send a POST request to the registration endpoint.
    response = client.post("/register/user", json=user)
    
    # Assert that the response status code is 201 (Created).
    assert response.status_code == 201
    
    # Assert that the response JSON matches the expected structure.
    assert response.json() == {
        "message": "user created",
        "user": {
            "username": "lyampayet",
            "email": "lyampayet@email.com",
        },
    }
