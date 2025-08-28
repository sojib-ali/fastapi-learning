from enum import Enum
from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, Header, Cookie, Request
from pydantic import BaseModel

app = FastAPI()


# @app.get("/")
# async def hello_world():
#     return {"hello": "world"}


#path parameter

@app.get("/users/{id}")
async def get_users(id:int = Path(..., ge=1 )):
    return {"id" : id}

class UserType(str, Enum):
    STANDARD = 'standard'
    ADMIN = "admin"

@app.get('/users/{type}/{id}')
async def get_user_and_type(type: UserType, id: int):
    return {"type": type, "id": id}

@app.get("/license-plates/{license}")
async def get_license_plate(license: str = Path(..., min_length=9, max_length=9)):
    return {"license": license}

# query parameters
@app.get("/users")
async def get_page(page: int =1, size: int = 10):
    return {"page": page, "size": size}

class UsersFormat(str, Enum):
    SHORT = "shot"
    FULL = "full"

@app.get("/users")
async def get_limited_value(format: UsersFormat):
    return {"format": format}

@app.get("/users")
async def get_validate_user(page: int = Query(1, gt = 0), size: int = Query(10, le = 10)):
    return {"page": page, "size": size}


class User(BaseModel):
    name: str
    age: int

class Company(BaseModel):
    name: str

@app.post("/users")
async def create_user(user: User, company: Company):
    return {"user": user, "company": company}

@app.post("/users")
async def  prioratize_user(user: User, priority: int = Body(..., ge = 1, le = 3)):
    return {"user": user, "priority": priority}

@app.post("/users")
async def create_form_user(name: str = Form(...), age: int = Form(...)):
    return {"name": name, "age": age}


# upload files
@app.post("/files")
async def upload_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# for large size file upload
@app.post("files")
async def upload_large_files(file: UploadFile = File(...)):
    return {"file_name": file.filename, "content-type": file.content_type}

#upload mulitple files
@app.post("files")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    return [
        {"file_name": file.filename, "content_type": file.content_type}
        
        for file in files
    ]

#headers
@app.get("/")
async def get_header(hello: str = Header(...)):
    return {"hello" : hello}

@app.get("/")
async def get_header_user_agent(user_agent: str = Header(...)):
    return {"user_agent": user_agent}

#cookies
@app.get("/")
async def get_cookie(hello:str | None = Cookie(None)):
    return {"hello": hello}

#the request object
@app.get("/")
async def get_reqeust_obj(request: Request):
    return {"path": request.url.path}


