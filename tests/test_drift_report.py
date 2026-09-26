import pandas as pd

from src.monitoring.drift_report import generate_drift_report


# ye test check krta hia ki unified report numeric or categorical dono ka drift
# ek sath correctly detect kr skti hai.
def test_generate_drift_report():
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "job": ["A"] * 50 + ["B"] * 50
    })

    current_df = pd.DataFrame({
        "age": [40] * 50 + [41] * 50, 
        "job": ["A"] * 20 + ["B"] * 80,
    })

    # numeric or categorical columns ko explicitly specify kr rhe hai,
    # taki report ko pata ho ki kis feature pr konsa test chalana hai.
    report = generate_drift_report(
        reference_df,
        current_df,
        ["age"],
        ["job"],
    )

    # age ki distribution change hui hai,
    # isliye numeric drift detect hona chahiye.
    assert report["numeric"]["age"]["drift_detected"] is True

    # job ki category distribution bhi change hui hai,
    # isliye categorical drift detect hoona chahiye.
    assert report["categorical"]["job"]["drift_detected"] is True