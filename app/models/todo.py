from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import TypedDict

class ToDo(BaseModel):
    """
    Data model for a ToDo-object.

    Attributes:
        id (UUID): unique identifier for the ToDo item
        title (str): title of the task (3 to 100 characters)
        description (str | None): optional description of the task
        done (bool): status flag indicating if the task is completed (default: False)
        created_at (datetime): timestamp of creation
    """
    id: UUID
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    done: bool = False
    created_at: datetime

class ToDoCreate(BaseModel):
    """
    Data model for a ToDoCreate-object (to create a ToDo-object).

    Attributes:
        title (str): title of the task
        description (str | None): optional description of the task
    """
    title: str
    description: str | None = None

class ToDoUpdate(BaseModel):
    """
    Data model for a ToDoUpdate-object (to update an existing ToDo-object).

    Attributes:
        title (str): updated title of the task
        description (str): updated description of the task
        done (bool): updated completion status
    """
    title: str
    description: str
    done: bool

class ToDoResponse(TypedDict):  
    """
    Typed dictionary for API responses containing ToDo data.

    Attributes:
        id (str): unique identifier, UUID4
        title (str): title of the task
        description (str): description of the task
        done (bool): completion status
        created_at (str): creation timestamp as string
    """
    id: str
    title: str
    description: str
    done: bool
    created_at: str