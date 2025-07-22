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

6. Write a Basic README.md which describes
   - what the project does
   - how to install dependencies
   - how to run the API

   


   