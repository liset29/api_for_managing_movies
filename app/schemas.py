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
    description: str

class FavoriteMovie(BaseModel):
    id: int
    kinopoisk_id: int



class TokenInfo(BaseModel):
    access_token: str
    token_type: str
