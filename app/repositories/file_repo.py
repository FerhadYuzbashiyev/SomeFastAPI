from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.file import File
from sqlalchemy import select

class FileRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, file: File) -> File:
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)

        return file
    
    async def get_file(self, file_id: int) -> File | None:
        stmt = select(File).where(File.id == file_id)
        result = await self.db.execute(stmt)
        file = result.scalar_one_or_none()
        return file
    