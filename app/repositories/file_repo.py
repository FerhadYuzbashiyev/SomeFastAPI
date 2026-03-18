from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.file import File
from app.dto.file_dto import FileCreateDTO

class FileRepository:

    @staticmethod
    async def create(db: AsyncSession, dto: FileCreateDTO) -> File:
        file = File(
            filename=dto.filename,
            content_type=dto.content_type,
            size=dto.size,
            path=dto.path,
            user_id=dto.user_id
        )

        db.add(file)
        await db.commit()
        await db.refresh(file)

        return file