from beanie import Document, init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, List, Optional, Type, TypeVar
from pydantic import BaseModel
from pydantic_settings import BaseSettings


from models.events import Event
from models.users import User

# Create a generic TypeVar that can be any Beanie Document.
# This will give you excellent type-hinting and autocompletion in your routes.
ModelType = TypeVar("ModelType", bound=Document)

class Settings(BaseSettings):
    # This is now a required setting. The app will not start if this is not defined in the environment.
    DATABASE_URL: str
    SECRET_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

async def initialize_database():
    """Initializes the database connection and Beanie."""
    settings = Settings()
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database=client.get_default_database(),
                      document_models=[Event, User])

class Database:
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def save(self, document: ModelType) -> None:
        """Saves a document to the collection."""
        await document.create()
    
    async def get(self, id: PydanticObjectId) -> Optional[ModelType]:
        """Retrieves a document by its ID."""
        doc = await self.model.get(id)
        return doc
    
    async def get_all(self) -> List[ModelType]:
        """Retrieves all documents from the collection."""
        docs = await self.model.find_all().to_list()
        return docs
    
    async def update(self, id: PydanticObjectId, body: BaseModel) -> Optional[ModelType]:
        """Updates a document by its ID."""
        doc = await self.get(id)
        if not doc:
            return None
        
        update_data = body.model_dump(exclude_unset=True)
        # The `update` method on a Beanie document instance performs an atomic
        # find-and-update operation and returns the updated document.
        await doc.update({"$set": update_data})
        return doc
    
    async def delete(self, id: PydanticObjectId) -> bool:
        """Deletes a document by its ID."""
        # Atomically finds and deletes the document in a single operation.
        delete_result = await self.model.find_one(self.model.id == id).delete()
        return delete_result is not None and delete_result.deleted_count > 0
    
    async def delete_all(self) -> int:
        """Deletes all documents from the collection."""
        delete_result = await self.model.delete_all()
        return delete_result.deleted_count