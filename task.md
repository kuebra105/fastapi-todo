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


2. Install the required packages:
   ```bash
   pip install fastapi uvicorn pydantic python-dotenv pytest

3. Add all dependencies to requirements.txt.

4. Make sure the following command runs your API
   ```bash
   uvicorn app.main:app --reload



   