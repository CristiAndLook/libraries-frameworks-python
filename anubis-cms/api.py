from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

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

# run the app with uvicorn in the terminal uvicorn api:app --reload 
print("API: anubis-cms/api.py")