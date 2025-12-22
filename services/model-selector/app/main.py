from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import ModelSuggestion
from .schemas import SuggestionResponse
from .selector import run_selection

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Model Selector Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/select", response_model=SuggestionResponse)
def select_models(dataset_id: int, file_name: str, db: Session = Depends(get_db)):

    problem_type, models = run_selection(file_name)

    suggestion = ModelSuggestion(
        dataset_id=dataset_id,
        problem_type=problem_type,
        suggested_models=models
    )

    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)

    return suggestion
