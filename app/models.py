from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    favorites = relationship("FavoriteMovie", back_populates="owner")

class FavoriteMovie(Base):
    __tablename__ = 'favorite_movies'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    kinopoisk_id = Column(Integer, nullable=False)
    owner = relationship("User", back_populates="favorites")
