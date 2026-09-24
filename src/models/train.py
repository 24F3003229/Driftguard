import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = "data/bank-full.csv"

NUMERIC_FEATURES = [
    "age", 
    "balance",
    "day",
    "duration",
    "campaign",
    "pdays",
    "previous",
]

CATEGORICAL_FEATURES = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "poutcome",
]

def load_data(path):
    return pd.read_csv(path, sep=";")

def prepare_data(df):
    X = df.drop(columns=["y"])

    y = df["y"].map({
        "no":0,
        "yes":1,
    })

    return X, y

def build_pipeline():
    numeric_pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore"),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    model = LogisticRegression(
        max_iter=1000
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    return pipeline

if __name__ == "__main__":
    df = load_data(DATA_PATH)

    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    pipeline = build_pipeline()

    pipeline.fit(X_train, y_train)

    joblib.dump(pipeline, "artifacts/baseline_model.joblib")
    print("Model saved to artifacts/baseline_model.joblib")

    print("Training completed.")
    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))

    y_pred = pipeline.predict(X_test)
    y_probability = pipeline.predict_proba(X_test)[:, 1]

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nAccuracy:")
    print(f"{accuracy_score(y_test, y_pred):.4f}")

    print("\nPrecision:")
    print(f"{precision_score(y_test, y_pred):.4f}")

    print("\nRecall:")
    print(f"{recall_score(y_test, y_pred):.4f}")

    print("\nF1-score:")
    print(f"{f1_score(y_test, y_pred):.4f}")

    print("\nROC-AUC:")
    print(f"{roc_auc_score(y_test, y_probability):.4f}")

    print("\nClassification report:")
    print(classification_report(y_test, y_pred))