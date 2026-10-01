from fastapi.testclient import TestClient
from src.api.app import app

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