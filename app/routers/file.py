from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.dependencies.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.file_service import FileService
from app.schemas.file_schema import FileResponse
from app.database.models.user import User
from app.database.models.file import File as FileModel
from app.schemas.task_schema import ConvertRequest
from sqlalchemy import select
from app.services.task_service import TaskService

router = APIRouter(prefix="/files", tags=["Files"])

service = FileService()

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return await service.upload_file(
        db=db,
        file=file,
        user_id=current_user.id
    )
    
@router.post("/{file_id}/convert")
async def convert_file(file_id: int, request: ConvertRequest, db: AsyncSession = Depends(get_db)):

    stmt = select(FileModel).where(FileModel.id == file_id)
    result = await db.execute(stmt)
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return await TaskService.convert_image(db, file, request.target_format)