## Part 1: Project Setup

1. Create a project using the structure below.
```bash
fastapi-todo/
├── app/
│ ├── main.py
│ ├── models/
│ │ └── todo.py
│ ├── routes/
│ │ └── todos.py
│ ├── dependencies/
│ │ └── config.py
│ ├── core/
│ │ └── storage.py
│ └── tests/
│ └── test_todos.py
├── .env
├── requirements.txt
└── README.md
```


2. Set Up a Virtual Environment. Use a virtual environment to manage dependencies locally:
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat

3. Install the necessary libraries:
   ```bash
   pip install fastapi uvicorn pydantic python-dotenv pytest

4. Add all dependencies to requirements.txt.

5. Make sure the following command runs your API:
   ```bash
   uvicorn app.main:app --reload


   In app/main.py, add the following basic FastAPI app:
   ```bash
   from fastapi import FastAPI
   app = FastAPI()
   @app.get("/")
   def read_root():
      return {"message": "Welcome to the FastAPI ToDo App!"}

## Part 2: Implement the ToDo API

### ToDo Model (`models/todo.py`)

Define a `ToDo` model using Pydantic:

```python
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ToDo(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    done: bool = False
```

Also create a `ToDoCreate` model (no `id`):

```python
class ToDoCreate(BaseModel):
    title: str
    description: Optional[str] = None
```
---
### In-Memory Storage (`core/storage.py`)

Use a dictionary to store tasks temporarily:

```python
from uuid import UUID
from typing import Dict
from app.models.todo import ToDo

storage: Dict[UUID, ToDo] = {}
```

### API Routes (`routes/todos.py`)

Implement the following endpoints:

| Method | Path               | Description                   |
|--------|--------------------|-------------------------------|
| GET    | `/todos`           | List all tasks                |
| GET    | `/todos/{id}`      | Get task by ID                |
| POST   | `/todos`           | Create new task               |
| PUT    | `/todos/{id}`      | Update existing task          |
| DELETE | `/todos/{id}`      | Delete task                   |
| GET    | `/todos/search`    | Filter tasks by `done: bool`  |

- use `HTTPException` for error handling when a task is not found.
- Add a timestamp (e.g. created_at) to each task
- Sort tasks by title or date
---
### Register Routes (`main.py`)

```python
from fastapi import FastAPI
from app.routes import todos

app = FastAPI(title="ToDo API")

app.include_router(todos.router, prefix="/todos", tags=["ToDos"])
```
---
## Part 3: Config via Environment Variables
### 📄 `.env` file
```env
APP_NAME=ToDo Manager
DEBUG=true
```

### Load Settings (`dependencies/config.py`)

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ToDo App"
    debug: bool = False

    class Config:
        env_file = ".env"
```

Use it in routes or endpoints:

```python
from fastapi import Depends
from app.dependencies.config import Settings

@app.get("/info")
def get_info(settings: Settings = Depends()):
    return {"app_name": settings.app_name, "debug": settings.debug}
```
---
## Part 4: Testing
Create unit tests using `pytest` in `tests/test_todos.py`.
Start with:
- Creating a new task
- Retrieving a task
- Deleting a task
- Handling errors (e.g., task not found)

Example:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos", json={"title": "Test Task"})
    assert response.status_code == 200
    assert "id" in response.json()
```
---
## Part 5: Documentation
- Access Swagger UI at: [`/docs`](http://localhost:8000/docs)
In your `README.md`, explain:
- How to run the API