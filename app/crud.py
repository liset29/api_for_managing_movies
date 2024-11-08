import base64

from app.auth import encode_jwt
from app.auth_utils import check_unique_value, hash_password
from app.models import User
from app.schemas import UserCreate, UserResponse


async def registration(user: UserCreate, session) -> UserResponse:
    '''Создаёт нового пользователя'''
    async with session() as session:
        await check_unique_value(session, user)
        password = await hash_password(user.password)
        password = base64.b64encode(password).decode("utf-8")

        new_user = User(
            username=user.username,
            password=password,
        )
        session.add(new_user)
        await session.commit()

        # jwt_payload = {"sub": user.username, "email": user.email}
        # await encode_jwt(jwt_payload)

        return new_user
