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

    def __init__(self, db: AsyncSession):
        self.user_repo=UserRepository(db)
        self.otp_repo=OTPRepository(db)

    async def create_user(self, dto: UserCreateDTO):
        user = User(
            name=dto.name,
            email=dto.email,
            password=hash_password(dto.password),
        )
        user = await self.user_repo.create(user)

        otp_code = random.randint(1000,9999)

        otp = OTP(
            user_id = user.id,
            otp_code = otp_code,
            expires_at = datetime.utcnow() + timedelta(minutes=500)
        )

        await self.otp_repo.create(otp)

        return {"message": "User created. OTP sent"}

    async def verify_and_get_token(self, dto: OTPCreateDTO):

        otp = OTP(
            user_id = dto.user_id,
            otp_code = dto.otp_code
        )

        otp_entity = await self.otp_repo.get_otp(otp)
        if not otp_entity:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        
        await self.otp_repo.delete_current_otp(otp_entity)
        await self.otp_repo.verify_user(otp_entity)
        token = create_access_token({"sub": str(dto.user_id)})

        return token

    async def login_user(self, email: str, password: str): 
        user_data = User(
            email = email,
            password = password
        )
        user = await UserRepository.get_by_email(user_data)

        if not user:
            return None
        if not verify_password(user_data.password, user.password):
            return None
        
        token = create_access_token({"sub": str(user.id)})
        return token
    
    async def delete_me(self, user: User):
        await UserRepository.delete(user)