# api/routers/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from services.user import UserService
from services.jwt import JwtService
from schemas.user import UserGet, UserCreate, UserUpdatePassword
from fastapi.responses import JSONResponse

# Create the user router
user_router = APIRouter()

@user_router.post("/", response_model=UserGet)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    
    # Call the create_user method of the UserService class
    return UserService.create_user(user, db)

@user_router.put("/password", response_class=JSONResponse)
def update_user(user: UserUpdatePassword, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Protected endpoint
    
    Update a user's password
    """
    
    # Call the update_user_password method of the UserService class
    UserService.update_user_password(current_user.id, user, db)
    # Return a JSONResponse indicating that the password has been updated
    return JSONResponse(status_code=200, content={"message": "Password updated"})