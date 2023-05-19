# main.py
from fastapi import FastAPI
from api.routers.user import user_router
from db import Base, engine

# Create the database tables if they do not exist yet
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# App routers
app.include_router(user_router, prefix="/user", tags=["User"])

@app.get("/")
async def root():
    """
    Root endpoint for the API that returns a simple message to verify that the API is running.
    """
    return {"message": "Hello World"}