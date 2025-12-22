from pydantic import BaseModel

class TrainResponse(BaseModel):
    id: int
    dataset_id: int
    model_name: str
    status: str
    model_path: str

    class Config:
        from_attributes = True
