import pandas as pd
from minio import Minio
import os

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

def download_dataset(object_name):
    path = f"/tmp/{object_name}"
    client.fget_object(os.getenv("MINIO_BUCKET_PROCESSED"), object_name, path)
    return path

def detect_problem(df):
    target = df.columns[-1]  # assume last column = label
    if df[target].dtype == "object" or df[target].nunique() < 20:
        return "classification"
    return "regression"

def suggest_models(problem_type):
    if problem_type == "classification":
        return ["RandomForest", "XGBoost", "SVM"]
    return ["LinearRegression", "XGBoostRegressor", "RandomForestRegressor"]

def run_selection(object_name):
    path = download_dataset(object_name)
    df = pd.read_csv(path)

    problem_type = detect_problem(df)
    models = suggest_models(problem_type)

    return problem_type, ",".join(models)
