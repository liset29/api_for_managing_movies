from fastapi import FastAPI


from .routers.users_router import users_router


app = FastAPI(title="Timurs Kino App")
app.include_router(users_router)
