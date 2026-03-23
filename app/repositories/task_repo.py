from app.database.models.processing_task import ProcessingTask, TaskStatus
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select

class ProcessingTaskRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, file_id: int) -> ProcessingTask:
        task = ProcessingTask(
            file_id=file_id,
            status=TaskStatus.queued
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task
    
    async def finish_task(self, task: ProcessingTask, result_path: str) -> ProcessingTask:
        task.status = TaskStatus.finished
        task.result_path = result_path
        task.finished_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(task)

        return task
    