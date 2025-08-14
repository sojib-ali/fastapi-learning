from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event

class User(BaseModel):
    email: EmailStr
    password: str
    # events: Optional[List[Event]] = []

    model_config={
        "json_schema_extra":{
            "example":{
                "email": "fastapi@packt.com",
                "password":"strong!!!",
            }
        }
    }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    model_config={
        "json_schema_extra":{
            "example":{
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }
    }