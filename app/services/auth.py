from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemes.auth import UserCreate
from passlib.context import CryptContext
from datetime import datetime, timezone
from app.core.security import verify_password, create_access_token
from datetime import timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# DOC: Service to authenticate user
async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


# DOC: Service to login user
async def login_user(db: AsyncSession, email: str, password: str):
    user = await authenticate_user(db, email, password)
    if not user:
        return None
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "document": user.document,
        "full_name": user.full_name,
        "email": user.email,
    }


# DOC: Service to get user by email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


# DOC: Service to create user
async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        document=user.document,
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        created=datetime.now(timezone.utc)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
