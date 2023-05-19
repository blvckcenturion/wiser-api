# schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator

class UserBase(BaseModel):
    """
    Base Pydantic model for a user
    """
    
    email: EmailStr = Field(..., description="Email address of the user")

class UserCreate(UserBase):
    """
    Pydantic model for creating a user
    """

    password: str = Field(..., description="Password of the user", max_length=255, min_length=8)
    password_confirmation: str = Field(..., description="Password confirmation of the user")

    @validator('password_confirmation')
    def passwords_match(cls, v, values, **kwargs):
        """
        Pydantic validator to check if the password and password confirmation match
        """
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserUpdatePassword(BaseModel):
    """
    Pydantic model for updating a user's password
    """

    old_password: str = Field(None, description="Password of the user", max_length=255, min_length=8)
    new_password: str = Field(None, description="Password of the user", max_length=255, min_length=8)
    new_password_confirmation: str = Field(None, description="Password confirmation of the user")

    @validator('new_password_confirmation')
    def passwords_match(cls, v, values, **kwargs):
        """
        Pydantic validator to check if the password and password confirmation match
        """
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserGet(UserBase):
    """
    Pydantic model for retrieving a user
    """
    
    id: int

    class Config:
        orm_mode = True
