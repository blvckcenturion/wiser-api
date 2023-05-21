# models/summarization.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel
from models.chat_entry import ChatEntryModel
from models.youtube_video_resource import YoutubeVideoResourceModel

class SummarizationModel(BaseModel):
    """
    Summarization model class that inherits from BaseModel and maps to the summarization table in the database.
    """

    # Table name
    __tablename__ = "summarization"

    # Model's specific attributes
    user_id = Column(Integer, ForeignKey('user.id'))
    youtube_video_resource_id = Column(Integer, ForeignKey('youtube_video_resource.id'))

    # Relationships
    user = relationship("UserModel", back_populates="summarizations")
    youtube_video_resource = relationship("YoutubeVideoResourceModel", back_populates="summarizations")
    chat_entries = relationship("ChatEntryModel", back_populates="summarization")