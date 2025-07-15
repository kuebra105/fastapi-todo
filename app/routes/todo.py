from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException, APIRouter
from pydantic import UUID4
from app.models.todo import ToDo, ToDoCreate, ToDoUpdate


router = APIRouter()
todos: dict[UUID4, ToDo] = {}

def get_time():    
    """
    Returns the current UTC timestamp.

    Returns:
        datetime: current date and time in UTC
    """
    return datetime.now(timezone.utc)


@router.post("/", response_model=ToDo)
def create_task(task: ToDoCreate):
    """
    Creates a new ToDo task if the title is unique.

    Args:
        task (ToDoCreate): task data to be created

    Returns:
        ToDo: the created ToDo object

    Raises:
        HTTPException: if a task with the same title already exists
    """
    task_id = uuid4()
    if any(t.title == task.title for t in todos.values()):
        raise HTTPException(status_code=400, detail="Task title already exists.")
    task_output = ToDo(
        id = task_id,
        title = task.title,
        description = task.description,
        done = False,
        created_at = get_time()
    )
    todos[task_id] = task_output
    return task_output

@router.get("/search", response_model=list[ToDo])
def get_task_by_done(done: bool = False):
    """
    Returns a list of tasks filtered by completion status.

    Args:
        done (bool): filter for completed (True) or open (False) tasks (default: False)

    Returns:
        list[ToDo]: list of filtered tasks
    """
    done_tasks = [t for t in todos.values() if t.done == done]
    return done_tasks

@router.get("/sorted_by_title", response_model=list[ToDo])
def get_tasks_sorted_by_title():
    """
    Returns all tasks sorted alphabetically by title.

    Returns:
        list[ToDo]: list of tasks sorted by title
    """
    return sorted(todos.values(), key=lambda t: t.title.lower())

@router.get("/sorted_by_date", response_model=list[ToDo])
def get_tasks_sorted_by_date(): 
    """
    Returns all tasks sorted by creation date.

    Returns:
        list[ToDo]: list of tasks sorted by creation timestamp
    """
    return sorted(todos.values(), key=lambda t: t.created_at)

@router.get("/{id}", response_model=ToDo)
def get_id_task(id: UUID4):
    """
    Returns a single task by its ID.

    Args:
        id (UUID4): unique identifier of the task

    Returns:
        ToDo: the requested task

    Raises:
        HTTPException: if the task is not found
    """
    task_to_see = todos.get(id)
    if task_to_see is None:
        raise HTTPException(status_code=404, detail="Task not found - nothing to see here.")
    return task_to_see

@router.get("/", response_model=list[ToDo])
def get_all_tasks():
    """
    Returns a list of all existing tasks.

    Returns:
        list[ToDo]: list of all tasks
    """
    return list(todos.values())

@router.put("/{id}", response_model=ToDo)
def update_task(id: UUID4, updated_task: ToDoUpdate): 
    """
    Updates an existing task by its ID.

    Args:
        id (UUID4): ID of the task to be updated
        updated_task (ToDoUpdate): updated task data

    Returns:
        ToDo: the updated task

    Raises:
        HTTPException: if the task is not found
    """
    task = todos.get(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found - nothing to see here.")
    task.title = updated_task.title
    task.description = updated_task.description
    task.done = updated_task.done
    return task

@router.delete("/{id}")
def delete_task(id: UUID4):
    """
    Deletes a task by its ID.

    Args:
        id (UUID4): ID of the task to be deleted

    Raises:
        HTTPException: if the task is not found
    """
    task_to_delete = todos.pop(id, None)
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found - nothing to see here.")