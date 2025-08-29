from datetime import date
from enum import Enum
from typing import Any, cast

from pydantic import BaseModel

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"

class Address(BaseModel):
    street_address: str
    postal_code : str
    city: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: list[str]
    address: Address

person = Person(
    first_name = "John",
    last_name = "Doe",
    gender = Gender.MALE,
    birthdate= date(1991, 1, 1),
    interests = ["travel", "sports"],
    address = Address(
        street_address = "Cole Valley",
        postal_code = "94117",
        city = "San Francisco",
        country = "US",
    ),
)

person_dict = person.model_dump()
print(person_dict["first_name"]) # "John"
print(person_dict["address"]["street_address"]) # "Cole Valley"

person_include = person.model_dump(include={"first_name", "last_name"})
print(person_include)

person_exclude = person.model_dump(exclude={"birthdate", "interests"})
print(person_exclude)

person_nested_include = person.model_dump(
    include = cast(Any, {
        "first_name": ...,
        "last_name": ...,
        "address": {"city", "country"},
    })
)