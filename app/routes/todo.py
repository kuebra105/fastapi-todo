from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException, APIRouter
from pydantic import UUID4
from app.models.todo import ToDo, ToDoCreate

router = APIRouter()
todos: list[ToDo] = []

def get_time():
    return datetime.now(timezone.utc)


@router.post("/", response_model=ToDo)
def create_task(task: ToDoCreate):
    if any(t.title == task.title for t in todos):
        raise HTTPException(status_code=400, detail="Task title already exists.")
    task_output = ToDo(
        id = uuid4(),
        title = task.title,
        description = task.description,
        done = False,
        created_at = get_time()
    )
    todos.append(task_output)
    return task_output

@router.get("/", response_model=list[ToDo])
def get_all_tasks():
    return todos

@router.get("/{id}", response_model=ToDo)
def get_id_task(task_id: UUID4):
    task_to_see = next((t for t in todos if t.id == task_id), None)
    if task_to_see is None:
        raise HTTPException(status_code=404, detail="Task not found — nothing to see here.")

@router.get("/sorted_by_title", response_model=list[ToDo])
def get_tasks_sorted_by_title():
    return sorted(todos, key=lambda t: t.title.lower())

@router.get("/sorted_by_date", response_model=list[ToDo])
def get_tasks_sorted_by_date():
    return sorted(todos, key=lambda t: t.created_at)

@router.get("/search", response_model=list[ToDo])
def get_task_by_done(done: bool = False) -> list[ToDo]:
    done_tasks = [t for t in todos if t.done == done]
    return done_tasks

@router.put("/{id}", response_model=ToDo)
def update_task(task_id: UUID4, updated_task: ToDo):
    if not any(t.id == task_id for t in todos):
        raise HTTPException(status_code=404, detail="Task not found - there is nothing to update.")
    for task in todos:
        if task.id == task_id:
            task.id = updated_task.id
            task.title = updated_task.title
            task.description = updated_task.description
            task.done = updated_task.done
            return updated_task

@router.delete("/{id}")
def delete_task(task_id: UUID4):
    task_to_delete = next((t for t in todos if t.id == task_id), None)
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found — nothing to see here.")
    todos.remove(task_to_delete)