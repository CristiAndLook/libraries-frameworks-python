from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, validator

import database as db
import helpers

# Models
class ModelClient(BaseModel):
    dni: constr(min_length=9, max_length=9)
    name: constr(min_length=2, max_length=30)
    last_name: constr(min_length=2, max_length=30)

class ModelClientCreate(ModelClient):
    @validator('dni')
    def validate_dni(cls, dni):
        if helpers.dni_validate(dni, db.Clients.list_clients):
            return dni
        raise ValueError('DNI already exists')
    


headers = {
    "Content-Type": "charset=utf-8",
}

# Create a FastAPI instance
app = FastAPI()

# Define a route
@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello, World!"}, headers=headers, media_type="application/json")

@app.get("/html")
async def html():
    return Response(content="<h1>Hello, World!</h1>", headers=headers, media_type="text/html")

@app.get("/clients/")
async def read_clients():
    content = [client.to_dict() for client in db.Clients.list_clients]
    return JSONResponse(content=content, headers=headers, media_type="application/json")

@app.get("/clients/{dni}")
async def read_client(dni: str):
    client = db.Clients.search_client(dni)
    if client:
        return JSONResponse(content=client.to_dict(), headers=headers, media_type="application/json")
    return JSONResponse(content={"message": "Client not found"}, headers=headers, media_type="application/json")

@app.post("/clients/create/")
async def create_client(client: ModelClientCreate):
    new_client = db.Clients.add_client(client.dni, client.name, client.last_name)
    if new_client:
        return JSONResponse(content=new_client.to_dict(), headers=headers, media_type="application/json")
    return JSONResponse(content={"message": "Client already exists"}, headers=headers, media_type="application/json")

@app.put("/clients/modify/")
async def modify_client(client: ModelClient):
    if db.Clients.search_client(client.dni):
        modified_client = db.Clients.modify_client(client.dni, client.name, client.last_name)
        if modified_client:
            return JSONResponse(content=modified_client.to_dict(), headers=headers, media_type="application/json")    
    raise HTTPException(status_code=404, detail="Client not found")

@app.delete("/clients/delete/")
async def delete_client(dni: str):
    if db.Clients.search_client(dni):
        deleted_client = db.Clients.delete_client(dni)
        if deleted_client:
            return JSONResponse(content=deleted_client.to_dict(), headers=headers, media_type="application/json")
    raise HTTPException(status_code=404, detail="Client not found")

# run the app with uvicorn in the terminal uvicorn api:app --reload 
print("API: anubis-cms/api.py")