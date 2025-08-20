from uuid import UUID
from app.models.todo import ToDo

storage: dict[UUID, ToDo] = {}