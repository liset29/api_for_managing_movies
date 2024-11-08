from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import encode_jwt, get_curresnt_active_auth_user
from app.auth_utils import validate_auth_user
from app.crud import registration
from app.db_helper import db_helper
from app.schemas import UserCreate, UserResponse, TokenInfo

http_bearer = HTTPBearer()

users_router = APIRouter(prefix="/user", tags=["USER"])


@users_router.post(
    "/login",
    response_model=TokenInfo,
    description="Endpoint that issues jwt token",
    response_description="Token",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def auth_user(user: UserCreate = Depends(validate_auth_user)):
    jwt_payload = {"sub": user.username}
    token = await encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@users_router.get(
    "/profile",
    description="Endpoint that shows the data of users who have passed authentication",
    response_description="User",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def auth_user_check(user: UserCreate = Depends(get_curresnt_active_auth_user)):
    user = UserResponse(
        username=user.username,
        id=user.id
    )
    return user


@users_router.post(
    "/register",

    description="Endpoint that creates user",
    response_description="New user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(
        user: UserCreate = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await registration(user, session)
    return user
