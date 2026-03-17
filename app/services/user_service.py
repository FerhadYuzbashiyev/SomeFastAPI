from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from app.database.models.user import User
from app.database.models.otp import OTP
from app.core.auth import hash_password, verify_password, create_access_token
from app.repositories.user_repo import UserRepository
from app.repositories.otp_repo import OTPRepository
from app.dto.user_dto import UserCreateDTO
from app.dto.otp_dto import OTPCreateDTO
from datetime import datetime, timedelta
from fastapi import HTTPException
import random

class UserService:

    @staticmethod
    async def create_user(db: AsyncSession, dto: UserCreateDTO):
        user = User(
            name=dto.name,
            email=dto.email,
            password=hash_password(dto.password),
        )
        user = await UserRepository.create(db, user)

        otp_code = random.randint(1000,9999)

        await OTPRepository.create(
            db,
            user.id,
            otp_code,
            datetime.utcnow() + timedelta(minutes=5)
        )

        return {"message": "User created. OTP sent"}

    @staticmethod
    async def verify_and_get_token(db: AsyncSession, dto: OTPCreateDTO):

        otp_entity = await OTPRepository.get_otp(db, dto.user_id, dto.otp_code)
        if not otp_entity:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        
        await OTPRepository.delete_current_otp(db, otp_entity.user_id)
        await OTPRepository.verify_user(db, otp_entity.user_id)
        token = create_access_token({"sub": str(dto.user_id)})

        return token

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def login_user(db: AsyncSession, email: str, password: str): 
        user = await UserRepository.get_by_email(db, email)

        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        
        token = create_access_token({"sub": str(user.id)})
        return token
    
    @staticmethod
    async def delete_me(db: AsyncSession, user: User):
        await UserRepository.delete(db, user)