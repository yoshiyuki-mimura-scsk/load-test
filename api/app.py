from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

@app.post("/auth/login")
def login(user: User):
    print(f"ユーザー '{user.username}'")
    return {
        "user_id": "user_id",
        "access_token": "dummy_token"
    }

@app.get("/users/{id}")
def user_info(id: str):
    print(f"ユーザー '{id}'")
    return {"id": id, "name": "user_name"}

@app.get("/tasks")
def tasks():
    return [
            {"id": "1", "name": "task1"},
            {"id": "2", "name": "task2"},
            {"id": "3", "name": "task3"}
        ]

@app.get("/dummy")
def dummy():
    return {"message": "Hello, this is dummy!"}
