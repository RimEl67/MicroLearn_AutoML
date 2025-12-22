from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

MODEL_PATH = "/models/model.pkl"

@app.get("/health")
def health():
    return {"status": "deployer running"}

@app.post("/deploy")
def deploy():
    return {"message": "Model ready for serving"}

@app.post("/predict")
async def predict(input: dict):
    model = joblib.load(MODEL_PATH)
    df = pd.DataFrame([input])
    prediction = model.predict(df)
    return {"prediction": prediction.tolist()}
