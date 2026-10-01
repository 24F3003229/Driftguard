from fastapi import FastAPI

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