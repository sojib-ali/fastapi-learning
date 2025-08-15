from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4

class Event(BaseModel):
    id: UUID = Field(default_factory = uuid4)
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    model_config ={
        "json_schema_extra":{
            "example":{
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the content of the FastAPI book in this event.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
                
            }
        }
    }