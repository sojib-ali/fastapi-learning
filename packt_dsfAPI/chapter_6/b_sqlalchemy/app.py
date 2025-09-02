import contextlib
from .database import create_all_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import FastAPI, Depends, HTTPException, Query, status
from . import schemas
from .models import Post

@contextlib.asynccontextmanager
async def lifespan(app:FastAPI):
    await create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/posts", response_model = schemas.PostRead, status_code = status.HTTP_201_CREATED)
async def create_post(post_create: schemas.PostCreate, session: AsyncSession = Depends(get_async_session)) -> Post:
    post = Post(**post_create.model_dump())
    session.add(post)
    await session.commit()

    return post