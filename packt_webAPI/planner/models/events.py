from pydantic import BaseModel
from typing import List

class Event(BaseModel):
    id: int
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
                "dexription": "We will be discussing the content of the FastAPI book in this event.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    }