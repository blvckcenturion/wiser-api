# models/youtube_video_resource.py
from models.base import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class YoutubeVideoResourceModel(BaseModel):
    """
    YoutubeVideoResource model class that inherits from BaseModel and maps to the youtube_video_resource table in the database.
    """

    # Table name
    __tablename__ = "youtube_video_resource"

    # Model's specific attributes
    title = Column(String(255), nullable=False)
    youtube_video_id = Column(String(255), unique=True, nullable=False)
    transcription_url = Column(String(1000), nullable=False)
    summarization_url = Column(String(1000), nullable=False)

    # Relationships
    summarizations = relationship("SummarizationModel", back_populates="youtube_video_resource")