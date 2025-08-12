from pydantic import BaseModel
from typing import List

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

class TodoItems(BaseModel):
    todos: List[TodoItem]

    model_config = {
        "json_schema_extra": {
            "example": {
                "todos": [
                    {
                        "item": "Example schema 1!"
                    },
                    {
                        "item": "Example shcema 2!"
                    }
                ]
            }
        }
    }
