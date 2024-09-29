from pydantic import BaseModel
from enum import Enum
from uuid import UUID, uuid4

class EnumPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    nonpriority = "nonpriority"

class Task(BaseModel):
    id: UUID = uuid4()
    title: str
    description: str
    completed: bool = False
    priority: EnumPriority = EnumPriority.nonpriority
