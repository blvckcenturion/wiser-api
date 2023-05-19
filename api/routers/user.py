# routers/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from services.user import UserService
from schemas.user import UserGet, UserCreate, UserUpdate

user_router = APIRouter()

@user_router.post("/", response_model=UserGet)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(user, db)