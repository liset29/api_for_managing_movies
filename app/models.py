from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    favorite_movies = relationship("FavoriteMovie", back_populates="user")


class FavoriteMovie(Base):
    __tablename__ = "favorite_movies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    kinopoisk_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    description = Column(String, nullable=False)
    rating = Column(Float, nullable=True)

    user = relationship("User", back_populates="favorite_movies")
