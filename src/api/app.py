from fastapi import FastAPI
from src.api.schemas import PredictionRequest
from src.api.predict import load_model, make_prediction

# Fast applicatioon create kr rhe hai.
app = FastAPI(
    title="DriftGuard API",
    description="API for ML model monitoring and drift detection.",
    version="1.0.0",
)

# basic health endpoint define kr rhe hai.
@app.get("/health")
def health_check():
    # API or monitoring service healthy hone ka response return kr rhe hai.
    return {
        "Status": "healthy",
    }

# saved baseline model ko API start hone pr load kr rhe hai.
# isse hr prediction request pr model ko dist se dobara load nhi krna pdega.
model = load_model()

# prediction endpoint define kr rhe hai.
# client POST request ke body me customer data bhejega.
@app.post("/predict")
def predict(request: PredictionRequest):
    # pydantic request object ko dictionary me convert kr rhe hai.
    input_data = request.model_dump()

    # landed model or input data ko prediction function me bhej rhe hai.
    result = make_prediction(model, input_data)

    # prediction or probability API response me return kr rhe hai.
    return result