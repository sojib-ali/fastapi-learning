from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])

user_database = Database(User)

@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already"
        )
    await user_database.save(user)
    return {
        "message": "User successfully registered!"
    }

@user_router.post("/signin")
async def sign_user(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if user_exist.password == user.password:
        return{
            "message": "User signed in successfully"
        }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Wrong credentials passed"
    )