from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

# for partialUpdate
class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int

class Post(PostBase):
    id: int
    nb_views: int = 0

class DummyDatabase:
    posts: dict[int, Post] = {}

db = DummyDatabase()

app = FastAPI()

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostRead)
async def create(post_create: PostCreate):
    new_id = max(db.posts.keys() or (0,)) + 1

    post = Post(id = new_id, **post_create.model_dump())

    db.posts[new_id] = post
    return post


# updaing an instance partially
@app.patch("/posts/{id}", response_model=PostRead)
async def partial_update(id: int, post_update: PostPartialUpdate):
    try:
        post_db = db.posts[id]

        updated_fields = post_update.model_dump(exclude_unset = True)
        updated_post = post_db.model_copy(update = updated_fields)

        db.posts[id] = updated_post
        return updated_post
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


