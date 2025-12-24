from pydantic import BaseModel, Field

class Book(BaseModel):
    # ... (Ellipsis) means the field is required - no default value is provided
    title: str = Field(..., min_length=1, max_length=100)
    # ... indicates this field must be provided when creating a Book instance
    author: str = Field(..., min_length=1, max_length=50)
    # ... ensures the year field is mandatory with no default value
    year: int = Field(..., gt=1900, lt=2100)


