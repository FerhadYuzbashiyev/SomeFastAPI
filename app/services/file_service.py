from app.repositories.task_repo import ProcessingTaskRepository
from app.repositories.file_repo import FileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.file_dto import FileCreateDTO
from app.dto.task_dto import ProcessingTaskCreateDTO
from app.database.models.file import File
from fastapi import HTTPException
from PIL import Image
import os, uuid

UPLOAD_DIR = "uploads"
SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "pdf", "webp"]

class FileService:

    def __init__(self, db: AsyncSession):
        self.file_repo = FileRepository(db)
        self.task_repo = ProcessingTaskRepository(db)

    async def upload_file(self, user_id: int, dto: FileCreateDTO):
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        unique_name = f"{uuid.uuid4()}_{dto.file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        content = await dto.file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        file = File(
            filename=dto.file.filename,
            content_type=dto.file.content_type,
            size=len(content),
            path=file_path,
            user_id=user_id
        )

        return await self.file_repo.create(file)
    
    async def convert_image(self, file_id: int, dto: ProcessingTaskCreateDTO):

        file_data = await self.file_repo.get_file(file_id)\
        
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        task = await self.task_repo.create(file_id)

        try:
            image = Image.open(file_data.path)
        except Exception:
            raise HTTPException(400, "File is not a valid image")

        if dto.target_format not in SUPPORTED_FORMATS:
            raise HTTPException(400, "Unsupported format")

        result_path = f"{file_data.path}.{dto.target_format}"

        if dto.target_format == "pdf":
            image = image.convert("RGB")
            image.save(result_path, "PDF")
        else:
            image.save(result_path, dto.target_format.upper())

        return await self.task_repo.finish_task(task, result_path)
    
    async def file_exists(self, file_id: int):
        return await self.file_repo.get_file(file_id)