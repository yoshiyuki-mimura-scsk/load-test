# ファイル名: app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/dummy")
def dummy():
    return {"message": "Hello, this is dummy!"}
