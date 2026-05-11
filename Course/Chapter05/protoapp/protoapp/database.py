from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(index=True)
    color: Mapped[str]

DATABASE_URL = "sqlite:///./production.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
# The SessionLocal is a class that will initialize the database session object
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

