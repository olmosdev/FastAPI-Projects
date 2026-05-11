import uvicorn
from protoapp.main import app

# $ python run_server.py
# $ python -m pdb run_server.py
# $ python -m pdb -m pytest tests
if __name__ == "__main__":
    uvicorn.run("protoapp.main:app", reload=True) # It's equivalent to $ uvicorn protoapp.main:app --reload


