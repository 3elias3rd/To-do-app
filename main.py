from fastapi import FastAPI
from fastapi.exceptions import HTTPException

app = FastAPI(title="To Do App")

@app.get("/")
def hello():
    return {"message": "hello world"}