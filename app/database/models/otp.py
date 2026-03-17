from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.database.base import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp_code = Column(Integer)
    expires_at = Column(DateTime)
