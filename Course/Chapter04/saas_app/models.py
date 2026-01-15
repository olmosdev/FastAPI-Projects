from enum import Enum

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


# Base class for SQLAlchemy 2.0 models. All tables must inherit from this.
class Base(DeclarativeBase):
    pass


# Enumeration for user roles. Inherits from str and Enum for strict typing.
# Stored as text in the DB ("basic" or "premium").
class Role(str, Enum):
    basic = "basic"
    premium = "premium"


# Represents the 'users' table in the database.
class User(Base):
    __tablename__ = "users"
    # Primary key, integer ID. Indexed for faster lookups.
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )
    # Unique constraints ensure no duplicate usernames or emails exist.
    username: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    # Stores the encrypted password hash, not the plain text password.
    hashed_password: Mapped[str]
    # User role, defaults to 'basic' if not specified.
    role: Mapped[Role] = mapped_column(
        default=Role.basic
    )
    # Secret for Time-based One-Time Password (2FA). Nullable as it may not be enabled initially.
    totp_secret: Mapped[str] = mapped_column(
        nullable=True
    )
