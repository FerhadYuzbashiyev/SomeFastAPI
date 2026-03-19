from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String(100))
    size = Column(Integer)
    path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="files")
    tasks = relationship("ProcessingTask", back_populates="files")