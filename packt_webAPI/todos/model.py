from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    item: str

class TodoItem(BaseModel):
    item: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "item": "Read the next chapter of the book"
            }
        }
    }
