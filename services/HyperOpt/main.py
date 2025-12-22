from fastapi import FastAPI
import optuna
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "hyperopt running"}

@app.post("/optimize")
async def optimize(data_path: str, target: str):
    df = pd.read_csv(data_path)
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    def objective(trial):
        n_estimators = trial.suggest_int("n_estimators", 50, 300)
        max_depth = trial.suggest_int("max_depth", 3, 20)

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth
        )

        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        return f1_score(y_test, preds, average="macro")

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=10)

    return {
        "best_params": study.best_params,
        "best_score": study.best_value
    }
