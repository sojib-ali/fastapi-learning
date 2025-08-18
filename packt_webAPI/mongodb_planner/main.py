from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.connection import initialize_database


from routes.users import user_router
from routes.events import event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await initialize_database()
    yield

app = FastAPI(lifespan=lifespan)    

## register routes
app.include_router(user_router, prefix='/user')
app.include_router(event_router, prefix='/event')


# origins = [
#  "http://packtpub.com",
#  "https://packtpub.com"
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)