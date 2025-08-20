# fastapi-todo
In this project, you'll build a RESTful API using **FastAPI** that simulates a basic ToDo task management system.

<br>

## How to install dependencies

1. The repository needs to be cloned:<br>
`git clone https://github.com/username/todo-fastapi.git`

2. Create virtual environment:<br>
`python -m venv venv`<br>
`venv\\Scripts\\activate`

3. Install dependencies in requirements.txt:
`pip install -r requirements.txt`
or manually install most important packages:<br>
`pip install fastapi uvicorn pydantic pydantic-settings httpx pytestv`

<br>

## What the project does

This FastAPI ToDo App provides a simple RESTful API that simulates a basic ToDo task management system.  
Users can create, view, update, and delete tasks, as well as filter them by completion status and sort them by title or creation date. 

It includes the API Endpoints:

| Method | Endpoint                         | Description                                                          |
|--------|----------------------------------|----------------------------------------------------------------------|
| GET    | `/`                              | returns a welcome message                                            |
| POST   | `/todos`                         | creates a new task with a unique title                               |
| GET    | `/todos`                         | returns a list of all tasks                                          |
| GET    | `/todos/{id}`                    | retrieves a task by its ID                                           |
| GET    | `/todos/search?done=true`        | filters tasks by completion status                                   |
| GET    | `/todos/sorted_by_title`         | returns all tasks sorted alphabetically by title                     |
| GET    | `/todos/sorted_by_date`          | returns all tasks sorted by creation date                            | 
| PUT    | `/todos/{id}`                    | updates an existing task by ID                                       |
| DELETE | `/todos/{id}`                    | deletes a task by ID                                                 |
| GET    | `/info`                          | returns basic application configuration (e.g., app name, debug mode) |


You can access the interactive API documentation via Swagger UI at /docs.

<br>

## How to run the API

1. Start the uvicorn server. <br>Make sure that all dependencies are installed and the virtual environment is active.<br>
`uvicorn app.main:app --reload`

2. Open API. <br>The API then runs at: http://127.0.0.1:8000

3. Open Swagger UI.<br>The interactive documentation can be found at: http://127.0.0.1:8000/docs

<br>

## How to test the API with Swagger UI

1) `GET /` - Test whether the API is accessible.<br>You will receive a welcome message: "Welcome to the FastAPI ToDo App!"

2) `POST /todos` - Create a few tasks.<br>Click on "Try it out" and enter data.

3) `GET /todos` - Displays all tasks.<br>You can check whether the tasks you created appear.

4) `GET /todos/{id}` - Display a specific task by its ID.<br>Copy the ID from a previous response and test this endpoint.

5) `GET /todos/search?done=true` - Filter tasks by status.<br>Set done=true or done=false and test the filter.

6) `GET /todos/sorted_by_title` - Sorts tasks alphabetically.<br>You can check whether the order is correct.

7) `GET /todos/sorted_by_date` - Sorts tasks by creation date.<br>You can check whether the order is correct.
