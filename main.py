# main.py
from fastapi import FastAPI
from api.routers.user import user_router
from api.routers.auth import auth_router
from api.routers.summarization import summarization_router
from db import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables if they do not exist yet
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Add a middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows CORS from this list of origins
    allow_credentials=True,  # Allows cookies to be sent with requests
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# App routers
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(summarization_router, prefix="/summarization", tags=["Summarization"])

@app.get("/")
async def root():
    """
    Root endpoint for the API that returns a simple message to verify that the API is running.
    """
    return {"message": "Hello World"}