from pydantic import BaseModel

class SuggestionResponse(BaseModel):
    id: int
    dataset_id: int
    problem_type: str
    suggested_models: str

    class Config:
        from_attributes = True
