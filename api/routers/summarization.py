# api/routers/summarization.py
from fastapi import APIRouter, Depends
from schemas.summarization import SummarizationCreate, SummarizationGet
from db import get_db
from services.jwt import JwtService
from sqlalchemy.orm import Session
from services.summarization import SummarizationService
from typing import List

summarization_router = APIRouter()

@summarization_router.post("/", response_model=SummarizationGet)
def create_summarization(summarization: SummarizationCreate, db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Create a new summarization
    """

    # Call the create_summarization method of the SummarizationService class
    return SummarizationService.generate_video_summarization(summarization, current_user.id, db)
    

@summarization_router.get("/", response_model=List[SummarizationGet])
def get_summarizations_by_user(db: Session = Depends(get_db), current_user = Depends(JwtService.get_current_user)):
    """
    Get list of summarizations
    """
    # Call the get_summarizations_by_user method of the SummarizationService class
    return SummarizationService.get_summarizations_by_user(current_user.id, db)