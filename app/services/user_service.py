from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from app.database.models.user import User
from app.core.auth import hash_password, verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.dto.user_dto import UserCreateDTO

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreateDTO):
        
        stmt = insert(User).values(
            name=user.name,
            email=user.email,
            password=hash_password(user.password)
        ).returning(User)

        result = await db.execute(stmt)
        await db.commit()

        db_user = result.scalar_one()
        return db_user
    
    @staticmethod
    async def get_users(db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int):
        stmt = delete(User).where(User.id == user_id)
        await db.execute(stmt)
        await db.commit()

    @staticmethod
    async def login_user(db: AsyncSession, email: str, password: str): 
        user = await UserRepository.get_by_email(db, email)

        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        
        token = create_access_token({"sub": str(user.id)})
        return token