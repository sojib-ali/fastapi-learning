from fastapi import FastAPI, Depends, Query, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

async def pagination(skip: int = 0, limit: int = 0) -> tuple[int, int]:
    return (skip, limit)

# complex dependecy function - 
async def com_pagination(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge = 0),
) -> tuple [int, int]: 
        capped_lmit = min(100, limit)
        return (skip, capped_lmit)


@app.get("/items")
async def list_items(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip" : skip, "limit": limit}

@app.get("/things")
async def list_things(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip" : skip, "limit": limit}


#getting an object or raising a 404 error
class Post(BaseModel):
     id: int
     title: str
     content: str

class PostUpdate(BaseModel):
     title: str | None = None
     content: str | None = None

class DummyDatabase:
     posts: dict[int, Post] = {}

db = DummyDatabase()

db.posts = {
     1: Post(id = 1, title="Post 1", content = "Content 1"),
     2: Post(id = 2, title="Post 2", content="Content 2"),
     3: Post(id = 3, title = "Post 3", content = "Content 3"),
}

async def get_post_or_404(id: int) -> Post:
     try:
          return db.posts[id]
     except KeyError:
          raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)

@app.get("/posts/{id}")
async def get(post: Post = Depends(get_post_or_404)):
     return post

@app.patch("/posts/{id}")
async def update(post_update: PostUpdate, post: Post = Depends(get_post_or_404)):
     update_data = post_update.model_dump(exclude_unset=True)
     updated_post = post.model_copy(update=update_data)
     db.posts[post.id] = updated_post
     return updated_post

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete(post: Post = Depends(get_post_or_404)):
    db.posts.pop(post.id)


# creating a class dependency
class Pagination:
    def __init__(self, maximum_limit: int = 100):
          self.maximum_limit = maximum_limit

    async def __call__(
        self,
        skip: int = Query(0, ge = 0),
        limit: int = Query(10, ge = 0),
        ) -> tuple[int, int]:
            capped_limit = min(self.maximum_limit, limit)
            return (skip, capped_limit)

pagination = Pagination(maximum_limit=50)

# Using class methods as dependecies

class NewPagination:
     def __init__(self, maximum_limit: int = 100):
          self.maximum_limit = maximum_limit

     async def skip_limit(
          self,
          skip: int = Query(0, ge = 0),
          limit: int = Query(10, ge = 0),
     ) -> tuple[int, int]:
               capped_limit = min(self.maximum_limit, limit)
               return (skip, capped_limit)
     
     async def page_size(
          self,
          page: int = Query(1, ge = 1),
          size: int = Query(10, ge = 0),
     ) -> tuple[int, int]:
          capped_size = min(self.maximum_limit, size)
          return (page, capped_size)
     
new_pagination = NewPagination(maximum_limit=50)

@app.get("/items")
async def newlist_items(p: tuple[int, int] = Depends(new_pagination.skip_limit)):
     skip, limit = p
     return {"skip": skip, "limit" : limit}

@app.get("/things")
async def new_things(p: tuple[int, int] = Depends(new_pagination.page_size)):
     page, size = p
     return {"page": page, "size": size}



     
