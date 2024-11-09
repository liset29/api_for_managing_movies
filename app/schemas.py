from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class Movie(BaseModel):
    kinopoisk_id: int
    title: str
    year: int
    description: str
    rating: Optional[str] = None



class FavoriteMovie(BaseModel):
    id: int
    kinopoisk_id: int


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class MoviesInfo(BaseModel):
    kinopoisk_id: int
    name: str
    year: str
    rating: str
