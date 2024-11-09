import base64

from app.auth import encode_jwt
from app.auth_utils import check_unique_value, hash_password
from app.kino_api import find_detail_movies
from app.models import User, FavoriteMovie
from app.schemas import UserCreate, UserResponse, Movie


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

        return new_user



async def add_favorite_movie(kino_id,user:UserCreate,session):
    film = await find_detail_movies(kino_id)
    async with session() as session:
        print(film)
        film = FavoriteMovie(user_id = user.id,
                             kinopoisk_id = kino_id,
                             title = film.get("nameRu"),
                             year = film.get('year'),
                             description = film.get('description'),
                             rating = film.get('ratingKinopoisk')
                             )

        session.add(film)
        await session.commit()

        movie = Movie(
            kinopoisk_id=film.kinopoisk_id,
            title=film.title,
            year=film.year,
            description=film.description,
            rating=film.rating
        )
        return movie

