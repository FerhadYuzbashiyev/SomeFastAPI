from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.file import File
from sqlalchemy import select

class FileRepository:

    @staticmethod
    async def create(db: AsyncSession, file: File) -> File:
        db.add(file)
        await db.commit()
        await db.refresh(file)

        return file
    
    @staticmethod
    async def get_file(db: AsyncSession, file_id: int) -> File:
        stmt = select(File).where(File.id == file_id)
        result = await db.execute(stmt)
        file = result.scalar_one_or_none()
        return file
    