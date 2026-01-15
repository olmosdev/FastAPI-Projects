from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection URL configuration (SQLite in this case)
SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"


# @lru_cache converts this function into an effective Singleton.
# Creates and returns the database engine only once.
@lru_cache
def get_engine():
    return create_engine(
        SQLALCHEMY_DATABASE_URL,
    )

# Generator for database session management.
def get_session():
    # Create a session factory configured without autocommit/autoflush
    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine(),
    )
    try:
        session = Session()
        # Yield the session to the caller (e.g., FastAPI route)
        yield session
    finally:
        # Ensure the session is closed upon completion, freeing resources
        session.close()