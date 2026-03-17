from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.database.models.user import User

class AdminService:

    @staticmethod
    async def get_users(db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int):
        stmt = delete(User).where(User.id == user_id)
        await db.execute(stmt)
        await db.commit()
