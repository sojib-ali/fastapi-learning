from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError
from typing import cast

class User(BaseModel):
    email: EmailStr
    website: HttpUrl

#Invalid email
try:
    User(email = "jdoe", website = cast(HttpUrl, "https://www.example.com"))
except ValidationError as e:
    print(str(e))

#Invalid URL
try:
    # User(email = "Jdoe@example.com", website = "jdoe") <-- error
    User(email = "Jdoe@example.com", website =cast(HttpUrl, "https://www.example.com") )
except ValidationError as e:
    print(str(e))

#valid
user = User(
    email = "jdoe@example.com",
    website = cast(HttpUrl, "https://www.example.com")
)

print(user)