from uuid import UUID
from app.models.todo import ToDo

storage: dict[UUID, ToDo] = {}
"""
Storage for ToDo objects with UUID.

Attributes:
    storage (dict[UUID, ToDo]): dictionary that stores unique UUIDs to ToDo objects.
"""