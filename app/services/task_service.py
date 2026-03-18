from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repo import ProcessingTaskRepository
from PIL import Image

class TaskService:

    @staticmethod
    async def convert_image(db: AsyncSession, file, target_format: str):

        task = await ProcessingTaskRepository.create(db, file.id)

        image = Image.open(file.path)

        result_path = f"{file.path}.{target_format}"

        image.save(result_path, target_format.upper())

        return await ProcessingTaskRepository.finish_task(db, task, result_path)