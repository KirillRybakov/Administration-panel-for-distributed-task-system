from domain.models import Task
from typing import Dict
from uuid import UUID, uuid4
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def hello_world():
    return {"msg":"Hi"}

id = uuid4()
print(id)

tasks: Dict[UUID, Task] = {
    id: Task(title="First", description="desc")
}

@router.get("/tasks", response_model=Dict[UUID, Task])
def get_task():
    return tasks




# @app.post("/tasks/create")
# def task_create(task: Task):
#     response = {
#         "description": task.description,
#         "priority": task.priority
#     }
#     
#     return{json.dump(response)}
