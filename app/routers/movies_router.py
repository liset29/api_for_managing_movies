from typing import List


from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import get_curresnt_active_auth_user
from app.crud import add_favorite_movie
from app.db_helper import db_helper
from app.kino_api import find_movies, find_detail_movies
from app.schemas import UserCreate, MoviesInfo, Movie

movies_router = APIRouter(prefix="/movies", tags=["MOVIES"])


@movies_router.get("/movies/search",
        description="Endpoint that shows information about films",
        response_description="Information about films",
        response_model=List[MoviesInfo],
        status_code=status.HTTP_200_OK,
)
async def search_movies( query: str = Query(..., description="Movie title to search"),
                        user: UserCreate = Depends(get_curresnt_active_auth_user)
):
    movies = await find_movies(query)
    return movies




@movies_router.get("/movies/{kinopoisk_id}",
        description="Endpoint that shows detail information about film",
        response_description="Information about film",
        response_model=dict,
        status_code=status.HTTP_200_OK,
)
async def search_movies(kino_id: int = Query(..., description="id film"),
                        user: UserCreate = Depends(get_curresnt_active_auth_user)
):
    detail_movies = await find_detail_movies(kino_id)
    return detail_movies



@movies_router.post('/movies/favorites',
        description='endpoint which adds to favorites',
        response_description='Information about film',
        response_model=Movie,
        status_code=status.HTTP_201_CREATED)
async def add_movie(kino_id: int = Query(..., description="id film"),
                    user: UserCreate = Depends(get_curresnt_active_auth_user),
                    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    result = await add_favorite_movie(kino_id,user,session)
    return result