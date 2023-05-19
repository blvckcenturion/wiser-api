# services/user.py
from schemas.user import UserCreate, UserGet, UserUpdatePassword
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import UserModel
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class UserService:
    """
    Service class for user related operations
    """

    @staticmethod
    def create_user(user: UserCreate, db: Session) -> UserGet:
        """
        Create a new user in the database

        Parameters
        ----------
        user : UserCreate
            Pydantic model for creating a user
        db : Session
            Database session

        Returns
        -------
        UserGet
            Pydantic model for retrieving a user
        """

        try:
            # Check if the email is already registered
            db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
            # If the email is already registered, raise an HTTPException
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            # If the email is not registered, create a new user
            new_user = UserModel(email=user.email)
            # password setter in the User model will hash the password
            new_user.password = user.password 
            # Add the new user to the database session and commit the changes
            db.add(new_user)
            db.commit()
            # Refresh the new user to get the updated id
            db.refresh(new_user)
            # Return the new user
            return new_user
        except SQLAlchemyError as e:
            # Rollback the changes if there is an error
            db.rollback()
            # Raise an HTTPException with the error message
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

    @staticmethod
    def update_user_password(id: int, user: UserUpdatePassword, db: Session):
        """
        Update a user's password in the database
        
        Parameters
        ----------
        id : int
            Id of the user
        user : UserUpdatePassword
            Pydantic model for updating a user
        db : Session
            Database session
        """
        try:
            # Get the user from the database
            db_user = db.query(UserModel).filter(UserModel.id == id).first()
            # If the user is not found, raise an HTTPException
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            # If the user is found, verify the password
            if not db_user.verify_password(user.old_password):
                raise HTTPException(status_code=400, detail="Invalid password")
            if user.old_password == user.new_password:
                raise HTTPException(status_code=400, detail="New password cannot be the same as old password")
            # If the password is verified, update the user
            for key, value in user.dict().items():
                setattr(db_user, key, value)
            # If the new password is provided, hash the new password
            if user.new_password:
                db_user.password = user.new_password
            # Commit the changes
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
