from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker
)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

"""
To define a model in SQLAlchemy, you need to create a base class 
that derives from the
DeclarativeBase class. This Base class maintains a catalog of 
classes and tables you’ve
defined and is central to SQLAlchemy’s ORM functionality
"""
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    email: Mapped[str]

Base.metadata.create_all(bind=engine)

"""
To manage sessions, we need to create a SessionLocal class. This 
class will be used to create and
manage session objects for the interactions with the database.

The sessionmaker function creates a factory for sessions. The 
autocommit and autoflush parameters are set to False, meaning 
you have to manually commit transactions and manage them
when your changes are flushed to the database.
"""
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

