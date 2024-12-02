from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.auth import create_user, get_user_by_email
from app.schemes.auth import UserCreate, UserResponse
from app.services.auth import login_user
from app.schemes.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login User",
    description="Authenticate a user and return an access token."
)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return an access token.
    - **email**: User email
    - **password**: User password
    """
    token_data = await login_user(
        db, email=request.email, password=request.password
    )
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Register User",
    description="Register a new user"
)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user
    - **document**: User document
    - **full_name**: User full name
    - **email**: User email
    - **password**: User password
    """
    existing_user = await get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user)
