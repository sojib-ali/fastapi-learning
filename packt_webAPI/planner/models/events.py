from sqlmodel import Field, SQLModel, JSON, Column
from typing import List, Optional
from uuid import UUID, uuid4


class Event(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the content of the FastAPI book in this event.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    }