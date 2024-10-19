from fastapi import Depends 
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import database.crud.tasks_crud as db
from database.database import get_session
from database.models import Task as DBTask
from domain.models import EnumPriority, TaskCreate, TaskUpdate, TaskOut
from typing import Dict
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException
from fastapi import Body

tasks_router = APIRouter()

@tasks_router.get("/")
async def hello_world():
    return {"msg":"Hi"}

id = uuid4()
print(id)

tasks: Dict[UUID, DBTask] = {
    id: DBTask(title="First", description="desc")
}

async def generate_random_task() -> DBTask:
    task_id = uuid4()
    return DBTask(
        id = task_id,
        title = f"Task {task_id}",
        description = "Randomly generated task",
        completed = False,
        priority = EnumPriority.nonpriority
    )

# for i in range(10):
#     task = generate_random_task()
#     tasks[task.id] = task

# Получение задач
@tasks_router.get("/tasks/all", response_model=Dict[str, TaskOut])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    result = await db.get_all_tasks(session)
    if not result:
        raise HTTPException(status_code = 404, detail = "Tasks not found):")
    
    tasks_dict = {
        str(task.id): {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority
        }
        for task in result
    }

    return JSONResponse(content = tasks_dict, status_code = 200)

# Получение задачи по ID
@tasks_router.get("/tasks/{task_id}", response_model = TaskOut)
async def get_task(task_id: str, session: AsyncSession = Depends(get_session)):
    #if task_id in tasks:
    #    return tasks[task_id]

    result = await db.get_task_by_id(session, task_id)
    if not result: 
        raise HTTPException(status_code = 404, detail = "Task not found")
    return JSONResponse(content={
        "id": str(result.id),
        "title": result.title,
        "description": result.description,
        "completed": result.completed,
        "priority": result.priority
    }, status_code=200)
    
# Создание новой задачи
@tasks_router.post("/task_create", response_model = TaskOut)
async def create_task(session: AsyncSession = Depends(get_session), data: TaskCreate = Body(...)):
    print(data)

    task_id = uuid4()
    new_task = DBTask(
        id = task_id,
        title = data.title,
        description = data.description,
        completed = False,
        priority = data.priority
    )
    tasks[task_id] = new_task

    success = await db.insert_task(session, new_task)
    if not success:
        raise HTTPException(status_code = 500, detail =  "Failed to create task")

    return new_task

# Обновление задачи по ID
@tasks_router.put("/task_update/{task_id}", response_model = TaskOut)
async def update_task(data: TaskUpdate, task_id: str, session: AsyncSession = Depends(get_session)):
    data = data.model_dump(exclude_unset=True)
    result = await db.update_task(session, task_id, data)
    if not result:
        raise HTTPException(status_code = 500, detail = "Failed to update task")
    data['id'] = task_id
    return data


@tasks_router.delete("/task_delete/{task_id}")
async def delete_task(task_id: str, session: AsyncSession = Depends(get_session)):
    result = await db.delete_task(session, task_id)
    if not result:
        raise HTTPException(status_code = 500, detail = "Failed to delete task")
    
    return JSONResponse(content={"status": "success", "task_id": task_id},
                        status_code=200)
