from fastapi import FastAPI
from app.routes.todo import router

app = FastAPI(title="ToDo API")

app.include_router(router, prefix="/todos", tags=["ToDos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI ToDo App!"}