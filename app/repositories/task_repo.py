from app.database.models.processing_task import ProcessingTask, TaskStatus
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.file import File
from datetime import datetime
from sqlalchemy import select

class ProcessingTaskRepository:

    @staticmethod
    async def create(db: AsyncSession, file_id: int) -> ProcessingTask:
        task = ProcessingTask(
            file_id=file_id,
            status=TaskStatus.queued
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task
    
    @staticmethod
    async def finish_task(db: AsyncSession, task: ProcessingTask, result_path: str) -> ProcessingTask:
        task.status = TaskStatus.finished
        task.result_path = result_path
        task.finished_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)

        return task
    