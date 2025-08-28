from enum import Enum
from pydantic import BaseModel, ValidationError
from datetime import date

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"

class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: list[str]

#Invalid gender
try:
    Person(
        first_name="Jhon",
        last_name="Doe",
        # gender="INVALID_VALUE",
        gender = Gender.MALE,
        birthdate=date(1991, 1, 1),
        interests=["travel", "sports"],
    )
except ValidationError as e:
    print(str(e))

#Invalid birthdate
try: 
    Person(
        first_name = "Jhon",
        last_name = "Doe",
        gender = Gender.MALE,
        birthdate= date(1991, 13, 42),
        interests = ["travel", "sports"],
    )
except ValidationError as e:
    print(str(e))


#valid
person = Person(
    first_name = "Jhon", 
    last_name = "Doe", 
    gender = Gender.MALE,
    birthdate = date(1991, 1, 1),
    interests = ["travel", "sports"],
)
print(person)

#Optional fileds and default values
class UserProfile(BaseModel):
    nickname: str
    location: str | None = None
    subscribed_newsletter: bool = True
