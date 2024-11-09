from fastapi import FastAPI

from .routers.movies_router import movies_router
from .routers.users_router import users_router


app = FastAPI(title="Timurs Kino App")
app.include_router(users_router)
app.include_router(movies_router)