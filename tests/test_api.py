from fastapi.testclient import TestClient
from src.api.app import app
from src.api.schemas import PredictionRequest

# FastAPI test client create kr rhe hai.
client = TestClient(app)

# ye tet verify krta hai ki health endpoint 
# correct HTTP response return krta hai.
def test_health_check():
    # /health endpoint ko request bhej rhe hai
    response = client.get("/health")

    # HTTP status code 200 hona chahiye.
    assert response.status_code == 200

    # Response me healthy status hona chahiye.
    assert response.json() == {
        "Status": "healthy",
    }

def test_predict():
    # prediction endpoint ke liye sample customer data bana rhe hai.
    input_data = {
        "age": 30,
        "job": "technician",
        "marital": "single",
        "education": "tertiary",
        "default": "no",
        "balance": 1500,
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "day": 15,
        "month": "may",
        "duration": 300,
        "campaign": 1,
        "pdays": -1,
        "previous": 0,
        "poutcome": "unknown",
    }

    # FastAPI ke TestClient se POST /predict request bhej rhe hai.
    response = client.post("/predict", json=input_data)

    # Successful API response ka status code 200 hona chahiye.
    assert response.status_code == 200

    # API response ko JSON me convert kr rhe hai.
    result = response.json()

    # Response me prediction or probability honi chahiye
    assert "prediction" in result
    assert "probability" in result

    # Prediction 0 ya 1 hona chahiye.
    assert result["prediction"] in [0, 1]

    # probability 0  or 1 ke bich honi chahiye
    assert 0 <= result["probability"] <= 1

def test_predict_invalid_input():
    # Invalid customer data bana rhe hai.
    # age integer hona chahiye, lekin yaha string bhej rhe hai.
    input_data = {
        "age": "hello",
        "job": "technician",
        "marital": "single",
        "education": "tertiary",
        "default": "no",
        "balance": 1500,
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "day": 15,
        "month": "may",
        "duration": 300,
        "campaign": 1,
        "pdays": -1,
        "previous": 0,
        "poutcome": "unknown",
    }

    # invalid data ke saath prediction request bhej rhe hai.
    response = client.post("/predict", json=input_data)

    # FastAPI/Pydantic ko invalid request reject krni chahiye.
    assert response.status_code == 422

def test_latest_report():
    # latest monitoring report ko API ke through request kr rhe hai.
    response = client.get("/reports/latest")

    # agr report available hai to API successfull response return kregi.
    assert response.status_code == 200

    # API response ko JSON dictionary me convert kr rhe hai.
    result = response.json()

    # Monitoring summary me ye important fields hone chahiye.
    assert "report_generated_at" in result
    assert "model_version" in result
    assert "reference_dataset" in result
    assert "overall_drift" in result
    assert "drifted_features" in result
    assert "overall_performance_degraded" in result
    assert "action" in result

def test_latest_report_not_found(monkeypatch):
    # API ke report loader ko temporarily replace kr rhe hai.
    # is test ke andr ye function pretend krega ki koi report nh hai.
    def fake_get_latest_monitoring_summary():
        raise FileNotFoundError("No monitoring reports found.")

    # original function ki jagah temporarily fake function use kr rhe hai
    monkeypatch.setattr(
        "src.api.app.get_latest_monitoring_summary",
        fake_get_latest_monitoring_summary,
    )

    # latest report endpoint ko request bhej rhe hai.
    response = client.get("/reports/latest")

    # Report available nhi hai, isliye API ko 404 return krna chahiye.
    assert response.status_code == 404

    # Error response ka detail verify kr rhe hai.
    assert response.json() == {
        "detail": "No monitoring reports found."
    }