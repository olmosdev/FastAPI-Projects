from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Request,
    status,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from protoapp.logging import client_logger
from protoapp.database import SessionLocal, Item

# To run this: $ uvicorn protoapp.main:app --reload
app = FastAPI()

@app.get("/home")
async def read_main():
    return {"message": "Hello World"}

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ItemSchema(BaseModel):
    name: str
    color: str

@app.post(
    "/item",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
def add_item(
    item: ItemSchema,
    db_session: Session = Depends(get_db_session),
):
    db_item = Item(name=item.name, color=item.color)
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return db_item.id

@app.get("/item/{item_id}", response_model=ItemSchema)
def get_item(
    item_id: int,
    db_session: Session = Depends(get_db_session),
):
    item_db = (
        db_session.query(Item)
        .filter(Item.id == item_id)
        .first()
    )
    if item_db is None:
        raise HTTPException(
            status_code=404, detail="Item not found"
        )

    return item_db

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_logger.info(
        f"method: {request.method}, "
        f"call: {request.url.path}, "
        f"ip: {request.client.host}"
    )
    response = await call_next(request)
    return response


