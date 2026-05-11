import pytest
from httpx import ASGITransport, AsyncClient

from protoapp.database import Item
from protoapp.main import app

"""
As a first check of the environment, we can try to collect the tests. From the protoapp root
project folder run: pytest --collect-only
After that, run: pytest
This specifies:
+ The configuration file pytest.ini
+ The pytest plugins used
+ The directory tests, the module test_main.py and the test test_read_main which
is a coroutine

All unit tests can be run from the terminal with the command: 
    $ pytest

A test can be run individually according to the test call syntax:
    $ pytest <test_module>.py::<test_name>

If we want to run the test function test_read_main_client, run:
$ pytest tests/test_main.py::test_read_main

We have a integration test called test_client_can_add_read_the_item_from_database
In the pytest.ini configuration we need to add the integration marker in the dedicated sections to register the mark.
Run:
    $ pytest -m integration -vv

Test coverage is a metric used in software testing to measure the extent to which the source code of
a program is executed when a particular test suite runs ($ pip install pytest-cov).
The way it works is quite straightforward. You need to pass the source code root, in our case the
protoapp directory, to the parameter --cov of pytest and tests root folder, in our case tests
as follows:
    $ pytest --cov protoapp tests
In addition (if you ran the previous command), a file named .coverage has been created. This is a binary file containing data on the test coverage and that can be used with additional tools to generate reports out of it.
    $ coverage html
If you ran the previous command, that should create a folder in the project root called "htmlcov".
Open index.html in the browser
"""

@pytest.mark.asyncio
async def test_read_main():
    client = AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )
    response = await client.get("/home")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World"
    }

def test_read_main_client(test_client):
    response = test_client.get("/home")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.integration
def test_client_can_add_read_the_item_from_database(
    test_client, test_db_session
):
    response = test_client.get("/item/1")
    assert response.status_code == 404

    response = test_client.post(
        "/item", json={"name": "ball", "color": "red"}
    )
    assert response.status_code == 201
    # Verify the user was added to the database
    item_id = response.json()
    item = (
        test_db_session.query(Item)
        .filter(Item.id == item_id)
        .first()
    )
    assert item is not None

    response = test_client.get("item/1")
    assert response.status_code == 200
    assert response.json() == {
        "name": "ball",
        "color": "red",
    }

