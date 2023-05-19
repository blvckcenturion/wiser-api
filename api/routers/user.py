# api/routers/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from services.user import UserService
from schemas.user import UserGet, UserCreate, UserUpdate

# Create the user router
user_router = APIRouter()

@user_router.post("/", response_model=UserGet)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    
    # Call the create_user method of the UserService class
    return UserService.create_user(user, db)