from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from database.connection import Database
from  models.events import Event, EventUpdate
from typing import List
from auth.authenticate import authenticate

event_database = Database(Event)

event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model = List[Event])
async def retrieve_all_events() -> List[Event]:
   events = await event_database.get_all()
   return events

@event_router.get("/{id}", response_model = Event)
async def retrieve_event(id: PydanticObjectId ) -> Event:

    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Event with supplied ID does not exist"
        )
    return event

@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await event_database.save(body)
    return {
        "message": "Event created successfully"
    }

@event_router.put("/{id}", response_model = Event)
async def update_event(id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)) -> Event:
    # First, retrieve the event to check for existence and ownership.
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    # Now, check if the authenticated user is the creator of the event.
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed. You are not the creator of this event."
        )
    # If all checks pass, perform the update.
    updated_event = await event_database.update(id, body)
    return updated_event

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    # First, retrieve the event to check for ownership before deleting.
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed. You are not the creator of this event."
        )
    await event.delete()
    return {"message": "Event deleted successfully"}

@event_router.delete("/")
async def delete_all_events(user: str = Depends(authenticate)) -> dict:
    # This is now safe: it only deletes events created by the authenticated user.
    delete_result = await Event.find(Event.creator == user).delete()
    return {"message": f"{delete_result.deleted_count} events deleted successfully."}