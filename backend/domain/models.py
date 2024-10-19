from pydantic import BaseModel
from enum import Enum, EnumType
from uuid import UUID, uuid4

class EnumPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    nonpriority = "nonpriority"

# class Task(BaseModel):
#     id: UUID = uuid4()
#     title: str
#     description: str = ""
#     completed: bool = False
#     priority: EnumPriority = EnumPriority.nonpriority

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: EnumPriority = EnumPriority.nonpriority

class TaskUpdate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    priority: EnumPriority = EnumPriority.nonpriority

class TaskOut(BaseModel):
    id: UUID
    title: str
    description: str = ""
    completed: bool = False
    priority: EnumPriority = EnumPriority.nonpriority

    class Config:
        orm_mode = True
