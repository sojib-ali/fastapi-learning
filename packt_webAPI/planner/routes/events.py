from fastapi import APIRouter, Body, HTTPException, status, Depends, Request
from database.connection import get_session
from  models.events import Event, EventUpdate
from sqlmodel import Session, select
from typing import List
from uuid import UUID

event_router = APIRouter(tags=["Events"])

events = []

@event_router.get("/", response_model = List[Event])
async def retrieve_all_events(session = Depends(get_session)) -> List[Event]:
   statement = select(Event)
   events = session.exec(statement).all()
   return events

@event_router.get("/{id}", response_model = Event)
async def retrieve_event(id: UUID, session = Depends(get_session)) -> Event:

    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Event with supplied ID does not exist"
    )

@event_router.post("/new")
async def create_event(new_event: Event,
                       session = Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {
        "message": "Event created successfully"
    }

@event_router.put("/edit/{id}", response_model = Event)
async def update_event(id: UUID, new_data: EventUpdate, session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.model_dump(exclude_unset = True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)

        return event
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Event with supplied ID does not exist")

@event_router.delete("/{id}")
async def delete_event(id: UUID) -> dict:
    for index, event in enumerate(events):
        if event.id == id:
            events.pop(index)
            return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail = "Event with supplied ID does not exist"
    )

@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return{
        "message": "Events deleted successfully"
    }