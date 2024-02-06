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
app = FastAPI(
    title="Anubis CMS",
    description="This is a simple example of a FastAPI app",
    version="0.1",
)

# Define a route

@app.get("/clients/", tags=["Clients"])
async def read_clients():
    content = [client.to_dict() for client in db.Clients.list_clients]
    return JSONResponse(content=content, headers=headers, media_type="application/json")

@app.get("/clients/{dni}", tags=["Clients"])
async def read_client(dni: str):
    client = db.Clients.search_client(dni)
    if client:
        return JSONResponse(content=client.to_dict(), headers=headers, media_type="application/json")
    return JSONResponse(content={"message": "Client not found"}, headers=headers, media_type="application/json")

@app.post("/clients/create/", tags=["Clients"])
async def create_client(client: ModelClientCreate):
    new_client = db.Clients.add_client(client.dni, client.name, client.last_name)
    if new_client:
        return JSONResponse(content=new_client.to_dict(), headers=headers, media_type="application/json")
    return JSONResponse(content={"message": "Client already exists"}, headers=headers, media_type="application/json")

@app.put("/clients/modify/", tags=["Clients"])
async def modify_client(client: ModelClient):
    if db.Clients.search_client(client.dni):
        modified_client = db.Clients.modify_client(client.dni, client.name, client.last_name)
        if modified_client:
            return JSONResponse(content=modified_client.to_dict(), headers=headers, media_type="application/json")    
    raise HTTPException(status_code=404, detail="Client not found")

@app.delete("/clients/delete/", tags=["Clients"])
async def delete_client(dni: str):
    if db.Clients.search_client(dni):
        deleted_client = db.Clients.delete_client(dni)
        if deleted_client:
            return JSONResponse(content=deleted_client.to_dict(), headers=headers, media_type="application/json")
    raise HTTPException(status_code=404, detail="Client not found")

# run the app with uvicorn in the terminal uvicorn api:app --reload 
print("API: anubis-cms/api.py")