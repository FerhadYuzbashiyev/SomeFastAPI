from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models.user import User

class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_email(self, user: User) -> User:
        result = await self.db.execute(select(User).where(User.email == user.email))
        user = result.scalar_one_or_none()
        return user
    
    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user: User):
        self.db.delete(user)
        await self.db.commit()
