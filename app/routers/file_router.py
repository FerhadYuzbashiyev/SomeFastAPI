from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.dependencies.auth import get_current_user
from app.schemas.task_schema import ConvertRequest
from app.services.file_service import FileService
from app.schemas.file_schema import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dto.file_dto import FileCreateDTO
from app.dto.task_dto import ProcessingTaskCreateDTO
from app.database.models.user import User
from app.database.session import get_db

router = APIRouter(prefix="/files", tags=["Files"])

service = FileService()

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dto = FileCreateDTO(file)
    return await service.upload_file(db, dto, current_user.id)
    
@router.post("/{file_id}/convert")
async def convert_file(
    file_id: int,
    request: ConvertRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
    ):
    
    dto = ProcessingTaskCreateDTO(
        target_format=request.target_format
    )

    file = await service.file_exists(db, file_id)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return await service.convert_image(db, file_id, dto)