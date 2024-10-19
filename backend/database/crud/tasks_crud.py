from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from typing import List

from database import models
import traceback
import logging

async def get_all_tasks(db: AsyncSession) -> List[models.Task]:
    try:
        result = (
            await db.execute(
                select(models.Task)
            )
        ).scalars().all()
        return result
    except Exception as e:
        logging.log(logging.ERROR, traceback.format_exc())
        return []
    finally:
        await db.close()

async def get_task_by_id(db: AsyncSession, id: str) -> models.Task | None:
    try:
        result = (
            await db.execute(
                select(models.Task)
                .filter(models.Task.id == id)
            )
        ).scalar_one_or_none()
        return result
    except Exception as e:
        logging.log(logging.ERROR, traceback.format_exc())
        return None
    finally:
        await db.close()


async def insert_task(db: AsyncSession, task: models.Task) -> bool:
    try:
        await db.execute(
            insert(models.Task)
            .values(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                priority=task.priority
            )
            .on_conflict_do_nothing(
                index_elements=["id"]
            )
        )
        await db.commit()
        return True
    except Exception as e:
        logging.log(logging.ERROR, traceback.format_exc())
        await db.rollback()
        return False
    finally:
        await db.close()


async def update_task(db: AsyncSession, id: str, task_data: dict) -> bool:
    try:
        await db.execute(
            update(models.Task)
            .where(models.Task.id == id)
            .values(
                title = task_data.get('title'),
                description = task_data.get('description'),
                completed = task_data.get('completed'),
                priority = task_data.get('priority')
            )
        )
        await db.commit()
        return True
    except Exception as e:
        logging.log(logging.ERROR, traceback.format_exc())
        await db.rollback()
        return False
    finally:
        await db.close()


async def delete_task(db: AsyncSession, id: str) -> bool:
    try:
        await db.execute(
            delete(models.Task)
            .where(models.Task.id == id)
        )
        await db.commit()
        return True
    except Exception as e:
        logging.log(logging.ERROR, traceback.format_exc())
        await db.rollback()
        return False
    finally:
        await db.close()
