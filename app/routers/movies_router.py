from typing import List
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import get_curresnt_active_auth_user
from app.crud import add_favorite_movie, delete_movie_from_favorite, get_all_movies
from app.db_helper import db_helper
from app.kino_api import find_movies, find_detail_movies
from app.schemas import UserCreate, Movie, ResponseDelete

movies_router = APIRouter(prefix="/movies", tags=["MOVIES"])


@movies_router.get("/search",
                   description="Endpoint to search for movies by title",
                   response_description="List of movies matching the search criteria",
                   response_model=List[Movie],
                   status_code=status.HTTP_200_OK)
async def search_movies(
    query: str = Query(..., description="Movie title to search"),
    user: UserCreate = Depends(get_curresnt_active_auth_user)
):
    return await find_movies(query)


@movies_router.get('/favorites',
                   description="Endpoint to get all user's favorite movies",
                   response_description="List of user's favorite movies",
                   response_model=List[Movie],
                   status_code=status.HTTP_200_OK)
async def get_all_favorite_movies(
    user: UserCreate = Depends(get_curresnt_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await get_all_movies(user, session)


@movies_router.get("/detail/{kinopoisk_id}",
                   description="Endpoint to get detailed information about a specific movie",
                   response_description="Detailed movie information",
                   response_model=dict,
                   status_code=status.HTTP_200_OK)
async def get_movie_detail(
    kinopoisk_id: int = Path(..., description="ID of the movie"),
    user: UserCreate = Depends(get_curresnt_active_auth_user)
):
    return await find_detail_movies(kinopoisk_id)


@movies_router.post('/favorites',
                    description='Endpoint to add a movie to favorites',
                    response_description='Information about the added movie',
                    response_model=Movie,
                    status_code=status.HTTP_201_CREATED)
async def add_movie_to_favorites(
    movie_id: int = Query(..., description="ID of the movie to add to favorites"),
    user: UserCreate = Depends(get_curresnt_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await add_favorite_movie(movie_id, user, session)


@movies_router.delete('/favorites/{kinopoisk_id}',
                      description='Endpoint to remove a movie from favorites',
                      response_description='Movie deletion status',
                      response_model=ResponseDelete,
                      status_code=status.HTTP_200_OK)
async def remove_movie_from_favorites(
    kinopoisk_id: int = Path(..., description="ID of the movie to remove from favorites"),
    user: UserCreate = Depends(get_curresnt_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await delete_movie_from_favorite(kinopoisk_id, user, session)
