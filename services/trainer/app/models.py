from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class TrainingRun(Base):
    __tablename__ = "training_runs"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer)
    model_name = Column(String)
    status = Column(String)
    model_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
