from fastapi import FastAPI, status, Response, Body, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from fastapi.staticfiles import StaticFiles

class Post(BaseModel):
    title: str
    nb_views: int = 0

class PublicPost(BaseModel):
    title: str

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent/"assets"), name="statc")


#post creation status_code = 201
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post

#when you delete an objece you have nothing to return
posts = {1: Post(title="hello", nb_views = 100),}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    posts.pop(id, None)
    return None


#the response model
@app.get("/posts/{id}", response_model=PublicPost)
async def get_data(id: int):
    return posts[id]

#the response parameter
#settng headers
@app.get("/")
async def custom_header(response: Response):
    response.headers["Custom-Header"] = "Custom-Header-value"
    return {"Hello": "world"}


#setting cookies
@app.get("/")
async def custom_cookies(response: Response):
    response.set_cookie("cookie-name", "cookie-value", max_age=86400)
    return {"hello": "world"}

#setting the status code dynamically
@app.put("/posts/{id}")
async def update_or_create_post(id: int, post: Post, response: Response):
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED
    posts[id] = post
    return posts[id]

#raising http error
@app.post("/password")
async def check_password(password: str = Body(...), passowrd_confirm : str = Body(...)):
    if password != passowrd_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail = {
                "message": "Password don't match",
                "hints": [
                    "check the caps lock on your keyboard", 
                    "Try to make the password visible by clicking on the eye icon to check your typing",
                ],
            },
        )
    return {"message": "Password match"}

#Building a custom response
#using the response_class argument

@app.get("/html", response_class=HTMLResponse)
async def get_html():

    return """
            <htmL>
                <head>
                    <title>Hello world!</title>
                </head>
                <body>
                    <h1>Hello world!</h1>
                </body>
            </html>
        """

@app.get("/text", response_class=PlainTextResponse)
async def text():
    return "Hello world!"

#making a redirection
@app.get("/redirection")
async def redirect():
    return RedirectResponse("/new-url", status_code = status.HTTP_301_MOVED_PERMANENTLY)

#erving a file
# @app.get("/cat")
# async def get_cat():
#     root_directory = Path(__file__).parent.parent
#     picture_path = root_directory / "assets" / "cat.jpg"
#     return FileResponse(picture_path)

#serve the superman image
@app.get("/cat")
async def get_cat():
    return RedirectResponse(url = "/static/superman.avif")