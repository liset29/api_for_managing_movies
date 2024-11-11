import base64

from fastapi import HTTPException
from sqlalchemy import select
from starlette import status
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


async def add_favorite_movie(movie_id:int, user: UserCreate, session) -> Movie:
    """Добавляет фильм в избранное пользователя, проверяя, не был ли он уже добавлен."""

    film_details = await find_detail_movies(movie_id)

    async with session() as session:
        existing_movie = await get_movie(movie_id, user, session)
        if existing_movie:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Этот фильм уже добавлен в избранное."
            )

        new_favorite_movie = FavoriteMovie(
            user_id=user.id,
            kinopoisk_id=movie_id,
            title=film_details.get("nameRu"),
            year=film_details.get('year'),
            description=film_details.get('description'),
            rating=film_details.get('ratingKinopoisk')
        )

        session.add(new_favorite_movie)
        await session.commit()

        movie = Movie(
            kinopoisk_id=new_favorite_movie.kinopoisk_id,
            title=new_favorite_movie.title,
            year=new_favorite_movie.year,
            description=new_favorite_movie.description,
            rating=new_favorite_movie.rating
        )

        return movie


async def delete_movie_from_favorite(movie_id: int, user: UserCreate, session):
    """Удаляет фильм из избранного пользователя, если он существует."""

    movie_to_delete = await get_movie(movie_id, user, session)

    if not movie_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Фильм с kino_id - {movie_id} не найден в избранном."
        )

    await session.delete(movie_to_delete)
    await session.commit()

    return {"detail": f"Фильм '{movie_id}' успешно удален из избранного."}


async def get_movie(movie_id: int, user: UserCreate, session):
    """Возвращает фильм из избранного пользователя по его kinopoisk_id."""

    stmt = select(FavoriteMovie).where(
        FavoriteMovie.kinopoisk_id == movie_id,
        FavoriteMovie.user_id == user.id
    )

    result = await session.execute(stmt)

    movie = result.scalars().first()

    return movie



async def get_all_movies(user: UserCreate, session):
    """Получает все фильмы из избранного пользователя, исключая информацию о user_id."""

    stmt = select(FavoriteMovie).where(FavoriteMovie.user_id == user.id)

    result = await session.execute(stmt)

    movies = result.scalars().all()

    movies_list = [
        {key: value for key, value in movie.__dict__.items() if key != "user_id"}
        for movie in movies
    ]

    return movies_list

