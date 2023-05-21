# models/user.py
from sqlalchemy import Column, String
from models.base import BaseModel
from sqlalchemy.orm import relationship
from models.summarization import SummarizationModel

import bcrypt

class UserModel(BaseModel):
    """
    User model class that inherits from BaseModel and maps to the user table in the database.
    """

    # Table name
    __tablename__ = "user"

    # Model's specific attributes
    email = Column(String(255), unique=True, nullable=False)
    _password = Column("password", String(255), nullable=False)

    # Relationships
    summarizations = relationship("SummarizationModel", back_populates="user")

    @property
    def password(self):
        """
        Getter method for the password field

        This property raises an AttributeError since the password attribute is not readable.
        """

        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Setter method for the password field

        This property hashes the password using bcrypt and stores the hash in the _password field.

        Parameters
        ----------
        password : str
            Password to hash
        """
        
        self._password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, password):
        """
        Verify the password hash against the password provided

        Parameters
        ----------
        password : str
        """

        return bcrypt.checkpw(password.encode("utf-8"), self._password.encode("utf-8"))
