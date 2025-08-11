from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class ToDo(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    done: bool = False
    created_at: datetime

class ToDoCreate(BaseModel):
    title: str
    description: str | None = None