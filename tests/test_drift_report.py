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

    # unified report me total monitored features ka count 
    # numeric + categorical features ka total hona chahiye.
    assert report["summary"]["total_features"] == 2

    # age or job dono me drift detect hau hai, isliye drifted featurs ki count 2 honi chahiye.
    assert report["summary"]["drifted_features"] == 2

    # kam se kam ek features drifted hone pr overall drifted status True hona chahiye.
    assert report["summary"]["overall_drift"] is True


# ye test check krta hai ki joab reference or current data same ho,
# to unified report correctly "no drift" report kre.
def test_generate_drift_report_no_drift():
    # reference data me baseline values define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "job": ["A"] * 50 + ["B"] * 50
    })

    # current data reference ke same hai
    # isliye kisi feature me distribution change nhi hui.
    current_df = reference_df.copy()

    # unified drift report generate kr rhe hai.
    report = generate_drift_report(
        reference_df,
        current_df,
        ["age"],
        ["job"],
    )

    # total monitored features 2 hona chahiye: 1 numeric + 1 categorical.
    assert report["summary"]["total_features"] == 2

    # koi feature drifted nhi hona chahiye.
    assert report["summary"]["drifted_features"] == 0

    # jab koi feature drifted nhi hai, overall drift bhi False hona chahiye.
    assert report["summary"]["overall_drift"] is False

    # individual numeric feature bhi non-drifted hona chahiye.
    assert report["numeric"]["age"]["drift_detected"] is False

    # individual categorical feature bhi no-drifted hoan chahiye.
    assert report["categorical"]["job"]["drift_detected"] is False