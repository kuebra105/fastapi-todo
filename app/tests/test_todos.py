from app.main import app
from fastapi.testclient import TestClient
from httpx import Response
from app.models.todo import ToDoResponse
from uuid import uuid4
from pydantic import TypeAdapter
from typing import TypeVar
import pytest


@pytest.fixture(autouse=True)
def clear_todos():
    """
    Fixture that clears the in-memory ToDo dict before each test. This ensures that each test runs isolated with a clean state.
    It empties the global 'todos' dict.
    """
    from app.routes.todo import todos
    todos.clear()


client = TestClient(app)


T = TypeVar("T")
def validate_response(response: Response, model: type[T]) -> T:
    return TypeAdapter(model).validate_python(response.json())

def test_create_todo():
    """
    Tests successful creation of a ToDo task.

    Asserts:
        - status code is 200
        - Response contains valid ToDo fields
        - task is marked as not done
    """
    response: Response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."}) # what the response should include
    assert response.status_code == 200 # assert: issue if condition is not ture
    data = validate_response(response, ToDoResponse)
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["description"] == "This task will be created."
    assert data["done"] is False
    assert "created_at" in data

def test_create_todo_duplicate_title_returns_400():
    """
    Tests failure when creating a task with a duplicate title.

    Asserts:
        - status code is 400
        - error message indicates duplicate title
    """
    _ = client.post("/todos", json={"title": "Test Task", "description": "First creation."})
    response: Response = client.post("/todos", json={"title": "Test Task", "description": "Second creation."}) # what the response should include
    assert response.status_code == 400 # assert: issue if condition is not ture  
    assert response.json()["detail"] == "Task title already exists."

def test_get_all_tasks(): 
    """
    Tests retrieval of all created tasks.

    Asserts:
        - status code is 200
        - Response is a list of tasks
        - all created task titles are present
    """
    _ = client.post("/todos", json={"title": "Task 1", "description": "First task"})
    _ = client.post("/todos", json={"title": "Task 2", "description": "Second task"})
    response: Response = client.get("/todos")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = validate_response(response, list[ToDoResponse])
    assert isinstance(data, list)
    assert len(data) == 2
    titles = [task["title"] for task in data]
    assert "Task 1" in titles
    assert "Task 2" in titles

def test_id_task():
    """
    Tests retrieval of a task by its ID.

    Asserts:
        - status code is 200
        - returned task matches the created ID and title
    """
    create_response: Response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."}) # task must be created to test get_id_task()
    created_task = validate_response(create_response, ToDoResponse)
    id = created_task["id"] # extract the ID from the JSON, that's the ID needed to test the GET-route
    response: Response = client.get(f"/todos/{id}") # testing with the extracted ID
    assert response.status_code == 200
    data = validate_response(response, ToDoResponse)
    assert data["id"] == id
    assert data["title"] == "Test Task"

def test_get_todo_with_nonexistent_id_returns_404():
    """
    Tests failure when retrieving a task with a non-existent ID.

    Asserts:
        - etatus code is 404
        - error message indicates task not found
    """
    id = str(uuid4())  # gültige UUID4, aber nicht in der Liste
    response: Response = client.get(f"/todos/{id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found - nothing to see here."

def test_get_tasks_sorted_by_date():
    """
    Tests sorting of tasks by creation date.

    Asserts:
        - status code is 200
        - tasks are returned in the order they were created
    """

    _ = client.post("/todos", json={"title": "Task 1", "description": "First task"})
    _ = client.post("/todos", json={"title": "Task 2", "description": "Second task"})
    response: Response = client.get("/todos/sorted_by_date")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = validate_response(response, list[ToDoResponse])
    assert len(data) == 2
    first_task = data[0]["title"]
    second_task = data[1]["title"]
    assert first_task == "Task 1"
    assert second_task == "Task 2"

def test_get_tasks_sorted_by_title():
    """
    Tests sorting of tasks alphabetically by title.

    Asserts:
        - status code is 200
        - tasks are sorted by title in ascending order
    """
    _ = client.post("/todos", json={"title": "Task B", "description": "B task"})
    _ = client.post("/todos", json={"title": "Task A", "description": "A task"})
    response: Response = client.get("/todos/sorted_by_title")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = validate_response(response, list[ToDoResponse])
    assert len(data) == 2
    first_task = data[0]["title"]
    second_task = data[1]["title"]
    assert first_task == "Task A"
    assert second_task == "Task B"

def test_get_task_by_done():
    """
    Tests filtering tasks by completion status.

    Asserts:
        - status code is 200
        - only completed tasks are returned
        - task marked as done is included in the result
    """
    done = client.post("/todos", json={"title": "Task 1", "description": "Task is done."})
    _ = client.post("/todos", json={"title": "Task 2", "description": "Task is not done."})
    created_task = validate_response(done, ToDoResponse)
    task_id = created_task["id"]
    _ = client.put(f"/todos/{task_id}", json={"title": "Task 1", "description": "Task is done.", "done": True})
    response: Response = client.get("/todos/search?done=true")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = validate_response(response, list[ToDoResponse])
    assert len(data) == 1
    done_task = data[0]["title"]
    assert done_task == "Task 1"
    assert data[0]["done"] == True

def test_update_task():
    """
    Tests updating an existing task.

    Asserts:
        - status code is 200
        - task fields are updated correctly
    """
    create_response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."})
    created_task = validate_response(create_response, ToDoResponse)
    id = created_task["id"] 
    response: Response = client.put(f"/todos/{id}", json={"title": "Test Task", "description": "This task will be delayed.", "done": False})
    assert response.status_code == 200
    # data: ToDoResponse = response.json()
    data = validate_response(response, ToDoResponse)
    assert data["id"] == id
    assert data["title"] == "Test Task"
    assert data["description"] == "This task will be delayed."
    assert data["done"] is False

def test_update_nonexistent_todo_returns_404():
    """
    Tests failure when updating a non-existent task.

    Asserts:
        - status code is 404
        - rrror message indicates task not found
    """
    id = str(uuid4())
    response: Response = client.put(f"/todos/{id}", json={"title": "Nonexistent Task", "description": "This task does not exist.", "done": False})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found - nothing to see here."

def test_delete_task():
    """
    Tests deletion of an existing task.

    Asserts:
        - status code is 200
        - task is no longer retrievable after deletion
    """
    create_response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."})
    created_task = validate_response(create_response, ToDoResponse)
    task_id = created_task["id"]
    response: Response = client.delete(f"/todos/{task_id}")
    assert response.status_code == 200
    get_response = client.get(f"/todos/{task_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Task not found - nothing to see here."

def test_delete_nonexistent_todo_returns_404():
    """
    Tests failure when deleting a non-existent task.

    Asserts:
        - status code is 404
        - error message indicates task not found
    """
    id = str(uuid4())
    response: Response = client.delete(f"/todos/{id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found - nothing to see here."
