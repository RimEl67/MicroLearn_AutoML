from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import uuid
import os

from .database import SessionLocal, engine
from .models import Base, Dataset
from .schemas import DatasetResponse
from .minio_client import upload_file
from .preprocessing import preprocess

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DataPreparer Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/prepare", response_model=DatasetResponse)
def prepare_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_id = str(uuid.uuid4())
    raw_path = f"/tmp/{file_id}.csv"
    processed_path = f"/tmp/{file_id}_processed.csv"

    with open(raw_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_file("raw-datasets", f"{file_id}.csv", raw_path)

    df = preprocess(raw_path)
    df.to_csv(processed_path, index=False)

    upload_file("processed-datasets", f"{file_id}_processed.csv", processed_path)

    dataset = Dataset(
        name=file.filename,
        path=f"{file_id}_processed.csv"
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset
