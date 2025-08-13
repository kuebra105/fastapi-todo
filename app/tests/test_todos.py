from app.main import app
from fastapi.testclient import TestClient
from httpx import Response
from typing import cast
from app.models.todo import ToDoResponse
from uuid import uuid4
import pytest


@pytest.fixture(autouse=True)
def clear_todos():
    from app.routes.todo import todos
    todos.clear()


client = TestClient(app)


def test_create_todo():
    response: Response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."}) # what the response should include
    assert response.status_code == 200 # assert: issue if condition is not ture
    # data: ToDoResponse = response.json()
    data = cast(ToDoResponse, response.json())
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["description"] == "This task will be created."
    assert data["done"] is False
    assert "created_at" in data

def test_FAIL_create_todo():
    _ = client.post("/todos", json={"title": "Test Task", "description": "First creation."})
    response: Response = client.post("/todos", json={"title": "Test Task", "description": "Second creation."}) # what the response should include
    assert response.status_code == 400 # assert: issue if condition is not ture  
    assert response.json()["detail"] == "Task title already exists."

def test_get_all_tasks(): 
    _ = client.post("/todos", json={"title": "Task 1", "description": "First task"})
    _ = client.post("/todos", json={"title": "Task 2", "description": "Second task"})
    response: Response = client.get("/todos")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = cast(list[ToDoResponse], response.json())
    assert isinstance(data, list)
    assert len(data) == 2
    titles = [task["title"] for task in data]
    assert "Task 1" in titles
    assert "Task 2" in titles

def test_id_task():
    create_response: Response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."}) # task must be created to test get_id_task()
    created_task = cast(ToDoResponse, create_response.json())
    id = created_task["id"] # extract the ID from the JSON, that's the ID needed to test the GET-route
    response: Response = client.get(f"/todos/{id}") # testing with the extracted ID
    assert response.status_code == 200
    # data: ToDoResponse = response.json()
    data = cast(ToDoResponse, response.json())
    assert data["id"] == id
    assert data["title"] == "Test Task"

def test_FAIL_id_task():
    id = str(uuid4())  # gültige UUID4, aber nicht in der Liste
    response: Response = client.get(f"/todos/{id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found — nothing to see here."

def test_get_tasks_sorted_by_date():
    _ = client.post("/todos", json={"title": "Task 1", "description": "First task"})
    _ = client.post("/todos", json={"title": "Task 2", "description": "Second task"})
    response: Response = client.get("/todos/sorted_by_date")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = cast(list[ToDoResponse], response.json())
    assert len(data) == 2
    first_task = data[0]["title"]
    second_task = data[1]["title"]
    assert first_task == "Task 1"
    assert second_task == "Task 2"

def test_get_tasks_sorted_by_title():
    _ = client.post("/todos", json={"title": "Task B", "description": "B task"})
    _ = client.post("/todos", json={"title": "Task A", "description": "A task"})
    response: Response = client.get("/todos/sorted_by_title")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = cast(list[ToDoResponse], response.json())
    assert len(data) == 2
    first_task = data[0]["title"]
    second_task = data[1]["title"]
    assert first_task == "Task A"
    assert second_task == "Task B"

def test_get_task_by_done():
    done = client.post("/todos", json={"title": "Task 1", "description": "Task is done."})
    _ = client.post("/todos", json={"title": "Task 2", "description": "Task is not done."})
    created_task = cast(ToDoResponse, done.json())
    task_id = created_task["id"]
    _ = client.put(f"/todos/{task_id}", json={"id": task_id, "title": "Task 1", "description": "Task is done.", "done": True})
    response: Response = client.get("/todos/search?done=true")
    assert response.status_code == 200
    # data: list[ToDoResponse] = response.json()
    data = cast(list[ToDoResponse], response.json())
    assert len(data) == 1
    done_task = data[0]["title"]
    assert done_task == "Task 1"
    assert data[0]["done"] == True

def test_update_task():
    create_response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."})
    created_task = cast(ToDoResponse, create_response.json())
    id = created_task["id"] 
    response: Response = client.put(f"/todos/{id}", json={"title": "Test Task", "description": "This task will be delayed.", "done": False})
    assert response.status_code == 200
    # data: ToDoResponse = response.json()
    data = cast(ToDoResponse, response.json())
    assert data["id"] == id
    assert data["title"] == "Test Task"
    assert data["description"] == "This task will be delayed."
    assert data["done"] is False

def test_FAIL_update_task():
    id = str(uuid4())
    response: Response = client.put(f"/todos/{id}", json={"id": id, "title": "Nonexistent Task", "description": "This task does not exist.", "done": False})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found - there is nothing to update."

def test_delete_task():
    create_response = client.post("/todos", json={"title": "Test Task", "description": "This task will be created."})
    created_task = cast(ToDoResponse, create_response.json())
    task_id = created_task["id"]
    response: Response = client.delete(f"/todos/{task_id}")
    assert response.status_code == 200
    get_response = client.get(f"/todos/{task_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Task not found — nothing to see here."

def test_FAIL_delete_task():
    id = str(uuid4())
    response: Response = client.delete(f"/todos/{id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found — nothing to delete here."