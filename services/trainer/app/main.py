from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import TrainingRun
from .schemas import TrainResponse
from .trainer_service import train

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trainer Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/train", response_model=TrainResponse)
def train_model(dataset_id: int, dataset_name: str, model_name: str, db: Session = Depends(get_db)):

    model_path = train(dataset_name, model_name)

    run = TrainingRun(
        dataset_id=dataset_id,
        model_name=model_name,
        status="completed",
        model_path=model_path
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    return run
