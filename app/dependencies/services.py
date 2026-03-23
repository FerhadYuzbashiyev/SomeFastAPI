from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.session import get_db
from app.services.file_service import FileService

def get_file_service(db: AsyncSession = Depends(get_db)) -> FileService:
    return FileService(db)
