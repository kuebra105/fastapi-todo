from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import TypedDict

class ToDo(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    done: bool = False
    created_at: datetime

class ToDoCreate(BaseModel):
    title: str
    description: str | None = None

class ToDoUpdate(BaseModel):
    title: str
    description: str
    done: bool

class ToDoResponse(TypedDict):
    id: str
    title: str
    description: str
    done: bool
    created_at: str