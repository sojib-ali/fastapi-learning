from fastapi import FastAPI, status
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    nb_views: int = 0

class PublicPost(BaseModel):
    title: str

app = FastAPI()


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