import bcrypt

from fastapi import Form, Depends
from app.db_helper import db_helper
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.models import User
from app.schemas import UserCreate


async def hash_password(password: str) -> bytes:
    '''Хеширует пароль с использованием bcrypt.'''
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def validate_password(password: str, hashed_password) -> bool:
    '''Проверяет, соответствует ли введённый пароль захешированному паролю.'''
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    '''Проверяет учетные данные пользователя (имя пользователя и пароль) для аутентификации.'''
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )

    user = await get_user(username, session)
    if not user:
        raise unauthed_exc

    valid_password =  validate_password(
        password=password,
        hashed_password=user.password)

    if not valid_password:
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")

    return user


async def get_user(value: str | int, session: AsyncSession):
    '''Получает пользователя из базы данных по имени пользователя или ID.'''
    if isinstance(value, str):
        stmt_username = select(User).where(User.username == value)
    else:
        stmt_username = select(User).where(User.id == value)

    result_username = await session.execute(stmt_username)
    user = result_username.scalars().first()

    return user




async def check_unique_value(session: AsyncSession, user: UserCreate):
    '''Проверяет уникальность имени пользователя и email'''
    stmt_username = select(User).where(User.username == user.username)
    result_username = await session.execute(stmt_username)
    existing_user_username = result_username.scalar_one_or_none()

    if existing_user_username:
        raise HTTPException(
            status_code=400, detail="A user with this username already registered")

    # stmt_email = select(User).where(User.email == user.email)
    # result_email = await session.execute(stmt_email)
    # existing_user_email = result_email.scalar_one_or_none()
    #
    # if existing_user_email:
    #     raise HTTPException(
    #         status_code=400, detail="A user with this email already registered")

    return True
