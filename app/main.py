from fastapi import FastAPI
from app.routes.todo import router
from app.routes import info

app = FastAPI(title="ToDo API")

app.include_router(router, prefix="/todos", tags=["ToDos"])
app.include_router(info.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI ToDo App!"}