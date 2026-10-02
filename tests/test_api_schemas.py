from src.api.schemas import PredictionRequest

def test_prediction_request_valid():
    request = PredictionRequest(
        age=30,
        job="technician",
        marital="single",
        education="tertiary",
        default="no",
        balance=1500,
        housing="yes",
        loan="no",
        contact="cellular",
        day=15,
        month="may",
        duration=300,
        campaign=1,
        pdays=-1,
        previous=0,
        poutcome="unknown",
    )

    assert request.age == 30
    assert request.job == "technician"