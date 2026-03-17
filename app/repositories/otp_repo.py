from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, select, update
from app.database.models.otp import OTP
from app.database.models.user import User
from datetime import datetime

class OTPRepository:

    @staticmethod
    async def create(db: AsyncSession, user_id: int, code: int, expires_at):

        await db.execute(
            delete(OTP).where(OTP.user_id == user_id)
        )

        await db.execute(
            insert(OTP).values(
                user_id=user_id,
                otp_code=code,
                expires_at=expires_at
            )
        )
        
        await db.commit()

    @staticmethod
    async def get_otp(db: AsyncSession, user_id: int, otp_code: int):
        stmt = select(OTP).where(
            OTP.user_id == user_id,
            OTP.otp_code == otp_code,
            OTP.expires_at > datetime.utcnow()
        )
    
        result = await db.execute(stmt)
        otp = result.scalar_one_or_none()
        return otp

    @staticmethod
    async def delete_current_otp(db: AsyncSession, user_id: int):
        await db.execute(delete(OTP).where(OTP.user_id == user_id))
        await db.commit()

    @staticmethod
    async def verify_user(db: AsyncSession, user_id: int):
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(emailVerifiedAt=datetime.utcnow())
        )

        await db.commit()
