from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.admin_service import AdminService
from app.dependencies.auth import get_current_admin
from app.database.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
async def admin_list_users(db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    return await AdminService.get_users(db)

@router.delete("/{user_id}")
async def delete(user_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    await AdminService.delete_user(db, user_id)
    return {"message": "User deleted"}

