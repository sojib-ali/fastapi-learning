from pydantic import BaseModel, Field, ValidationError

class Person(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length = 3)
    age: int | None = Field(None, ge = 0, le = 120)

#Invalid first name
try:
    Person(
        first_name = "j", 
        last_name = "Doe",
        age = 30
    )
except ValidationError as e:
    print(str(e))


#Invalid age
try:
    Person(
        first_name = "Jhon",
        last_name = "Doe",
        age = 2000
    )
except ValidationError as e:
    print(str(e))

#valid
person = Person(
    first_name = "John",
    last_name="Doe",
    age=30
)
print(person)