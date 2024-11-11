from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class Movie(BaseModel):
    kinopoisk_id: int
    title: Optional[str]
    year: Optional[Union[float, str]]
    description: Optional[str] = None
    rating: Optional[Union[float, str]] = None


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class ResponseDelete(BaseModel):
    detail: str
