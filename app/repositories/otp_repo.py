from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, select, update
from app.database.models.otp import OTP
from app.database.models.user import User
from datetime import datetime

class OTPRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, otp: OTP) -> OTP:

        await self.db.execute(delete(OTP).where(OTP.user_id == otp.user_id))

        await self.db.add(otp)
        await self.db.commit()
        await self.db.refresh(otp)

    async def get_otp(self, otp: OTP) -> OTP:
        stmt = select(OTP).where(
            OTP.user_id == otp.user_id,
            OTP.otp_code == otp.otp_code,
            OTP.expires_at > datetime.utcnow()
        )
    
        result = await self.db.execute(stmt)
        otp = result.scalar_one_or_none()
        return otp

    async def delete_current_otp(self, otp: OTP) -> OTP:
        await self.db.execute(delete(OTP).where(OTP.user_id == otp.user_id))
        await self.db.commit()

    async def verify_user(self, otp: OTP) -> OTP:
        await self.db.execute(
            update(User)
            .where(User.id == otp.user_id)
            .values(email_verified_at=datetime.utcnow())
        )

        await self.db.commit()
