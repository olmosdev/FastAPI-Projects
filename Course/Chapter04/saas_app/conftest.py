import pytest
from passlib.context import CryptContext
from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Role, User

# Security configuration for password hashing in tests.
# We need this to insert users with valid hashed passwords into the test database.
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


# Fixture to create a fresh database session for each test.
@pytest.fixture
def session():
    # Create an in-memory SQLite engine.
    # 'check_same_thread=False' is needed because FastAPI/Starlette runs in a different thread context during tests.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=QueuePool,
    )

    # Create a session factory bound to the in-memory engine.
    session_local = sessionmaker(engine)

    # Instantiate a new session.
    db_session = session_local()

    # Create all tables defined in the SQLAlchemy models.
    Base.metadata.create_all(bind=engine)

    # Yield the session to the test function.
    yield db_session

    # Teardown: Drop all tables and close the session after the test finishes.
    Base.metadata.drop_all(bind=engine)

    db_session.close()


# Fixture to pre-populate the database with sample users.
# This is useful for testing read operations or permissions without creating users manually in every test.
@pytest.fixture(scope="function")
def fill_database_session(session):
    # Add a basic user 'johndoe'
    (
        session.add(
            User(
                username="johndoe",
                email="johndoe@email.com",
                hashed_password=pwd_context.hash(
                    "pass1234"
                ),
                role=Role.basic,
            )
        ),
    )
    # Add another basic user 'chrissophia'
    (
        session.add(
            User(
                username="chrissophia",
                email="chrissophia@email.com",
                hashed_password=pwd_context.hash(
                    "hardpass"
                ),
                role=Role.basic,
            )
        ),
    )
    # Add a premium user 'manucourtney'
    (
        session.add(
            User(
                username="manucourtney",
                email="mcourtney@email.com",
                hashed_password=pwd_context.hash(
                    "harderpass"
                ),
                role=Role.premium,
            )
        ),
    )
    # Commit the transaction to save these users to the in-memory database.
    session.commit()
    # Yield the session containing the data.
    yield session