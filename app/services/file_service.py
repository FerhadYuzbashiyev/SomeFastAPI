from app.repositories.task_repo import ProcessingTaskRepository
from app.repositories.file_repo import FileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.file_dto import FileCreateDTO
from app.dto.task_dto import ProcessingTaskCreateDTO
from app.database.models.file import File
from fastapi import UploadFile
from PIL import Image
import os, uuid

UPLOAD_DIR = "uploads"

class FileService:

    @staticmethod
    async def upload_file(db: AsyncSession, dto: FileCreateDTO, user_id: int):

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        unique_name = f"{uuid.uuid4()}_{dto.file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)
        with open(file_path, "wb") as buffer:
            buffer.write(await dto.file.read())

        file = File(
            filename=dto.file.filename,
            content_type=dto.file.content_type,
            size=dto.file.size if hasattr(file, "size") else 0,
            path=file_path,
            user_id=user_id
        )

        return await FileRepository.create(db, file)
    
    @staticmethod
    async def convert_image(db: AsyncSession, file_id: int, dto: ProcessingTaskCreateDTO):

        file_data = await FileRepository.get_file(db, file_id)
        task = await ProcessingTaskRepository.create(db, file_id)

        image = Image.open(file_data.path)

        result_path = f"{file_data.path}.{dto.target_format}"

        image.save(result_path, dto.target_format.upper())

        return await ProcessingTaskRepository.finish_task(db, task, result_path)
    
    @staticmethod
    async def file_exists(db: AsyncSession, file_id: int):
        return await FileRepository.get_file(db, file_id)