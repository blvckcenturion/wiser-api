from pydantic import BaseModel, Field
from typing import Optional

class SummarizationCreate(BaseModel):
    """
    Pydantic model for creating a summarization
    """
    
    youtube_video_url: str = Field(..., description="Youtube video URL of the video to be summarized")

class SummarizationGet(BaseModel):
    """
    Pydantic model for retrieving a summarization
    """
    
    id: int
    title: str
    youtube_video_id: str

    
    class Config:
        orm_mode = True