from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from email_validator import (
    EmailNotValidError,
    validate_email,
)

from models import User, Role

# Security configuration: Use bcrypt for hashing passwords.
# 'deprecated="auto"' allows upgrading hashes if the scheme changes in the future.
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)

def add_user(
    session: Session,
    username: str,
    password: str,
    email: str,
    role: Role = Role.basic,
) -> User | None:
    # Hash the plain text password before storing it.
    hashed_password = pwd_context.hash(password)

    # Create the User model instance.
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )
    # Add the user to the session (staging area).
    session.add(db_user)
    try:
        # Commit the transaction to save to the DB and refresh to get generated IDs/defaults.
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        # IntegrityError handles attempts to add a username or email that already exists.
        # Rollback cleans the session state after the error.
        session.rollback()
        return
    return db_user

def get_user(
    session: Session, username_or_email: str
) -> User | None:
    try:
        validate_email(username_or_email)
        query_filter = User.email
    except EmailNotValidError:
        query_filter = User.username
    user = (
        session.query(User)
        .filter(query_filter == username_or_email)
        .first()
    )
    return user



