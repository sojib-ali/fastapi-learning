from pydantic import BaseModel

#repetative method
class RepPostCreate(BaseModel):
    title: str
    content: str

class RepPostRead(BaseModel):
    id: int
    title: str
    content: str

class RepPost(BaseModel):
    id: int
    title: str
    content: str
    nb_views: int = 0

#using model-inheritance
class PostBase(BaseModel):
    title: str
    content: str

    def excerpt(self) -> str:
        return f"{self.content[:140]}..."

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int

class Post(PostBase):
    id: int
    nb_views: int = 0