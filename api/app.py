# ファイル名: app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/dummy")
def dummy():
    return {"message": "Hello, this is dummy!"}

@app.post("/auth/login")
def login():
    return {"access_token": "dummy_token"}

@app.get("/test")
def test():
    return {"message": "Hello, this is test!"}
