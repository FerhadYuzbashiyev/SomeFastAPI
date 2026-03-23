from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, OtpCreate
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user
from app.database.models.user import User
from app.dto.user_dto import UserCreateDTO
from app.dto.otp_dto import OTPCreateDTO
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

service = UserService()

@router.post("/")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    dto = UserCreateDTO(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return await service.create_user(db, dto)

@router.post("/verify")
async def verify(otp: OtpCreate, db: AsyncSession = Depends(get_db)):

    dto = OTPCreateDTO(
        user_id=otp.user_id,
        otp_code=otp.otp_code
    )

    token = await service.verify_and_get_token(db, dto)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# @router.get("/", response_model=list[UserResponse])
# async def list_users(db: AsyncSession = Depends(get_db)):
#     return await UserService.get_users(db)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.delete("/me")
async def delete_me(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="No such user")
    await service.delete_me(db, current_user)

@router.get("/{user_id}", response_model=UserResponse)
async def get(user_id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_user(db, user_id)

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await service.login_user(db, user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }
