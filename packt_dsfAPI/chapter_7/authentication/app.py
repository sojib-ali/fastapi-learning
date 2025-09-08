import contextlib
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authentication import schemas
from database import create_all_tables, get_async_session
from models import User, AccessToken
from sqlalchemy.ext.asyncio import AsyncSession
from password import get_password_hash
from sqlalchemy import exc, select
from authentication import authenticate, create_access_token
from datetime import datetime, timezone

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield

app = FastAPI()

@app.post(
    "/register", status_code = status.HTTP_201_CREATED, response_model = schemas.UserRead
)
async def register(
    user_create: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)
) -> User:
    hashed_password = get_password_hash(user_create.password)
    user = User(
        **user_create.model_dump(exclude={"password"}), hashed_password = hashed_password
    )

    try:
        session.add(user)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail = "Email alread exists"
        )
    return user

@app.post("/token")
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    session: AsyncSession = Depends(get_async_session),
):
    email = form_data.username
    password = form_data.password
    user = await authenticate(email, password, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = await create_access_token(user, session)

    return {"access_token": token.access_token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    query = select(AccessToken).where(
        AccessToken.access_token == token,
        AccessToken.expiration_date >= datetime.now(tz= timezone.utc,),
    )
    result = await session.execute(query)
    access_token: AccessToken | None = result.scalar_one_or_none()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return access_token.user

@app.get("/protected-route", response_model = schemas.UserRead)
async def protected_route(user: User = Depends(get_current_user))
    return user