# models/chat_entry.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel


class ChatEntryModel(BaseModel):
    """
    ChatEntry model class that inherits from BaseModel and maps to the chat_entry table in the database.
    """

    # Table name
    __tablename__ = "chat_entry"

    # Model's specific attributes
    summarization_id = Column(Integer, ForeignKey('summarization.id'))
    input_text = Column(String(255), nullable=False)
    output_text = Column(String(255), nullable=False)

    # Relationships
    summarization = relationship("SummarizationModel", back_populates="chat_entries")