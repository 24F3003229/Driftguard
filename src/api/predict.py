import joblib
import pandas as pd

# Trained baseline model ka location define kr rhe hai.
MODEL_PATH = "artifacts/baseline_model.joblib"

def load_model(model_path=MODEL_PATH):
    # saved .joblib file se trained model load kr rhe hai
    model = joblib.load(model_path)

    # loaded model ko return kr rhe hai taaki prediction ke liye use ho ske.
    return model

def make_prediction(model, input_data):
    # dictionary ko ek-row pandas DataFrame me convert kr rhe hai.
    # model ko vhi feature structure chahiye jo training ke time use hua tha.
    input_df = pd.DataFrame([input_data])

    # model se class prediction le rhe hai.
    # EXAMPLE: 0 ya 1.
    prediction = model.predict(input_df)[0]

    # class 1 ki probability nikal rhe hai.
    # [0][1] ka matlab:
    # first (and only) row -> class 1 ki probability.
    probability = model.predict_proba(input_df)[0][1]

    # API ke liye prediction or probability ko dictionary me return kr rhe hai.
    return {
        "prediction": int(prediction),
        "probability": float(probability),
    }