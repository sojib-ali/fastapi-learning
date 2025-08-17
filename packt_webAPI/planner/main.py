from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
from database.connection import conn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    conn()
    yield
    # Code to run on shutdown

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")