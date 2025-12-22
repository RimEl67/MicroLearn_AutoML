from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class ModelSuggestion(Base):
    __tablename__ = "model_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer)
    problem_type = Column(String)
    suggested_models = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
