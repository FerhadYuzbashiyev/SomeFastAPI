from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.user_service import UserService
from app.core.auth import get_current_user
from app.database.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(db, user)


@router.get("/", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await UserService.get_users(db)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.get_user(db, user_id)


@router.delete("/{user_id}")
async def delete(user_id: int, db: AsyncSession = Depends(get_db)):
    await UserService.delete_user(db, user_id)
    return {"message": "User deleted"}


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await UserService.login_user(db, user.email, user.password)
    if not token:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }