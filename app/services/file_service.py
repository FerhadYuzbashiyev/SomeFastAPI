import os, uuid
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.file_dto import FileCreateDTO
from app.repositories.file_repo import FileRepository

UPLOAD_DIR = "uploads"

class FileService:

    @staticmethod
    async def upload_file(db: AsyncSession, file: UploadFile, user_id: int):

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        dto = FileCreateDTO(
            filename=file.filename,
            content_type=file.content_type,
            size=file.size if hasattr(file, "size") else 0,
            path=file_path,
            user_id=user_id
        )

        return await FileRepository.create(db, dto)