import os
import pandas as pd
from io import BytesIO
from minio import Minio
import joblib
import mlflow
import mlflow.sklearn
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from xgboost import XGBClassifier, XGBRegressor

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

BUCKET = os.getenv("MINIO_BUCKET_MODELS")
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

def download_dataset(file_name):
    path = f"/tmp/{file_name}"
    client.fget_object("processed-datasets", file_name, path)
    return pd.read_csv(path)

def is_classification(y):
    return y.nunique() < 20 or y.dtype == "object"


############ PYTORCH MODEL ###########
class SimpleNN(nn.Module):
    def __init__(self, in_features):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.layers(x)

######################################


def train(dataset_name, model_name):
    df = download_dataset(dataset_name)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    classification = is_classification(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    mlflow.start_run()

    if classification:
        if model_name == "RandomForest":
            model = RandomForestClassifier()
        elif model_name == "XGBoost":
            model = XGBClassifier()
        elif model_name == "SVM":
            model = SVC()
        else:
            model = RandomForestClassifier()

        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        score = accuracy_score(y_test, preds)
        mlflow.log_metric("accuracy", score)

    else:
        if model_name == "RandomForest":
            model = RandomForestRegressor()
        elif model_name == "XGBoost":
            model = XGBRegressor()
        else:
            model = RandomForestRegressor()

        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        score = r2_score(y_test, preds)
        mlflow.log_metric("r2", score)

    model_bytes = BytesIO()
    joblib.dump(model, model_bytes)
    model_bytes.seek(0)

    object_name = f"{model_name}_model.pkl"
    client.put_object(BUCKET, object_name, model_bytes, len(model_bytes.getvalue()))

    mlflow.sklearn.log_model(model, "model")
    mlflow.end_run()

    return object_name
