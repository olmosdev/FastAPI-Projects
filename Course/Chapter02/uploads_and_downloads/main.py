from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/uploadfile")
async def upload_file(
    # ... = placeholder (Ellipsis operator)
    file: UploadFile = File(...) # ... = File(required=True)
):
    return {"filename": file.filename}


