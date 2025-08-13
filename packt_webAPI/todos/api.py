from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from todos.todo import todo_router

app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {'message': "Hello world"}

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(todo_router)

