from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Enum
from app.database.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class TaskStatus(str, enum.Enum):
    queued = "queued"
    processing = "processing"
    finished = "finished"
    failed = "failed"
    
class ProcessingTask(Base):
    __tablename__ = "processing_tasks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.queued)
    result_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    file_id = Column(Integer, ForeignKey("files.id"))
    files = relationship("File", back_populates="tasks")
