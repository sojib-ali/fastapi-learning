from datetime import date
from pydantic import BaseModel, ValidationError, field_validator, model_validator, EmailStr

#Applying validation at the field level
class Person(BaseModel):
    first_name: str
    last_name: str
    birthdate: date

    @field_validator("birthdate")
    def valid_birthdate(cls, v:date):
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v
    

#Invalid birthdate
try:
    Person(first_name="John", last_name="Doe", birthdate=date(1800, 1, 1))
except ValidationError as e:
    print(str(e))

#valid
person = Person(first_name = "John", last_name= "Doe", birthdate= date(1991, 1, 1))
print(person)

#Applying validation at the object level
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @model_validator(mode = "after")
    def password_match(cls, values):
        password = values.get("password")
        password_confirmation = values.get("password_confirmation")

        if password != password_confirmation:
            raise ValueError("Passwords don't match")
        return values
    
# passwords not matchin
try:
    UserRegistration(
        email = "jdoe@example.com", password="aa", password_confirmation="bb"
    )
except ValidationError as e:
    print(str(e))

#valid
user_registration = UserRegistration(
    email="jdoe@example.com", password="aa", password_confirmation="aa"
)

print(user_registration)

#Applying validation before Pydantic parsing
class Model(BaseModel):
    values: list[int]

    @field_validator("values", mode = "before")
    def split_string_values(cls, v):
        if isinstance(v, str):
            # return v.split(",")
            return [int(x) for x in v.split(",") if x]
        return v
    
# m = Model(values = "1,2,3")
m = Model.model_validate({"values": "1, 2, 3"})
print(m.values) #[1, 2, 3]

