import router_example
from fastapi import FastAPI

# uvicorn main:app --reload -> http://127.0.0.1:8000
app = FastAPI()
app.include_router(router_example.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}