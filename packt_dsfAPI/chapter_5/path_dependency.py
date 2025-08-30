from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, status

app = FastAPI()

def secret_header(secret_header: str | None = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    
# adding dependencies in the path decorator arguments
@app.get("/protected-route", dependencies= [Depends(secret_header)])
async def protected_route():
    return {"hello": "world"}

# adding dependency in the router method arguments

router = APIRouter(dependencies=[Depends(secret_header)])

@router.get("/route1")
async def router_route1():
    return {"route": "route1"}

@router.get("/route2")
async def router_route2():
    return {"route": "route2"}

app = FastAPI()
app.include_router(router, prefix = "/router")

# set the dependecies argument on the include_router method
app.include_router(router, prefix = "/router", dependencies= [Depends(secret_header)])

# set the dependencies on a whole application
app = FastAPI(dependencies= [Depends(secret_header)])

