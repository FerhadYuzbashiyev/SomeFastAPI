from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.dependencies.auth import get_current_user
from app.schemas.task_schema import ConvertRequest
from app.services.file_service import FileService
from app.schemas.file_schema import FileResponse
from app.dto.file_dto import FileCreateDTO
from app.dto.task_dto import ProcessingTaskCreateDTO
from app.database.models.user import User
from app.database.session import get_db
from app.dependencies.services import get_file_service

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...), 
    service: FileService = Depends(get_file_service),
    user: User = Depends(get_current_user)
):
    dto = FileCreateDTO(file)
    return await service.upload_file(user.id, dto)
    
@router.post("/{file_id}/convert")
async def convert_file(
    file_id: int,
    request: ConvertRequest,
    service: FileService = Depends(get_file_service),
    user: User = Depends(get_current_user)
    ):
    
    dto = ProcessingTaskCreateDTO(
        target_format=request.target_format
    )

    return await service.convert_image(file_id, dto)