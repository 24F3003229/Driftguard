import pandas as pd
from src.monitoring.monitoring_report import (
    generate_monitoring_report,
)

# ye test verify krta hai ki unified monitoring report 
# drift or perfomance reports ko correctly combine kr rhe hai.
def test_generate_monitoring_report():
    # reference dataset me 4 numeric features define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "balance": [100] * 50 + [101] * 50,
        "day": [1] * 50 + [2] * 50,
        "campaign": [1] * 50 + [2] * 50,
    })

    # current dataset copy hai reference dataset ki
    current_df = reference_df.copy()

    # sirf age feature me intentional drift introduce kr rhe hai.
    current_df["age"] = [40] * 50 + [41] * 50

    # reference model performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # current model performance me recall or F1 ko 
    # intentionally decrease kr rhe hai.
    current_metrics = {
        "accuracy": 0.89,
        "precision": 0.63,
        "recall": 0.28,
        "f1_score": 0.39,
        "roc_auc": 0.88,
    }

    # unified monitoring repot generate kr rhe hai.
    report = generate_monitoring_report(
        reference_df,
        current_df,
        ["age", "balance", "day", "campaign"],
        [],
        reference_metrics,
        current_metrics,
    )

    # age me drift detect hona chahiye.
    assert report["drift"]["summary"]["drifted_features"] == 1

    # model performance me degradation detect honi chahiye.
    assert (
        report["performance"]["summary"]["overall_performance_degraded"]
        is True
    )

    # drift or performance dono presend hone ki vjh se
    # final action evaluate_retraining hona chahiye.
    assert report["decision"]["action"] == "evaluate_retraining"

# ye integration test verify krta hai ki jab
# data drift or performance degradation dono nhi hai,
# unified report no_action return krta hai.
def test_generate_monitoring_report_no_action():
    # reference data define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "balance": [100] * 50 + [101] * 50,
    })

    # current data reference ke exactly same hai.
    current_df = reference_df.copy()

    # reference model performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # current performance bhi same hai.
    current_metrics = reference_metrics.copy()

    # unified monitoring report generate kr rhe hai.
    report = generate_monitoring_report(
        reference_df,
        current_df,
        ["age", "balance"],
        [],
        reference_metrics,
        current_metrics,
    )

    # koi data drift nhi hona chahiye.
    assert report["drift"]["summary"]["overall_drift"] is False

    # koi performance degradation nhi hona chahiye.
    assert (
        report["performance"]["summary"]["overall_performance_degraded"] 
        is False
    )

    # isliye final action no_action hona chahiye.
    assert report["decision"]["action"] == "no_action"

# ye integration test verify krta hai ki sirf data drift hone pr
# unified report investigate action return krti hai.
def test_generate_monitoring_report_investigate():
    # reference data define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "balance": [100] * 50 + [101] * 50,
    })
    #current data reference data ki copy hai
    current_df = reference_df.copy()

    # sirf age me intentional drift introduce kr rhe hai.
    current_df["age"] = [40] * 50 + [41] * 50

    # reference performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # current performance same rakhi hai
    # isliye performancec degradation nhi hogi.
    current_metrics = reference_metrics.copy()

    # unified monitoring report generate kr rhe hai
    report = generate_monitoring_report(
        reference_df,
        current_df,
        ["age", "balance"],
        [],
        reference_metrics,
        current_metrics,
    )

    # data drift detect hona chahiye
    assert report["drift"]["summary"]["overall_drift"] is True

    # performance degradation nhi honi chahiye.
    assert (
        report["performance"]["summary"]["overall_performance_degraded"]
        is False
    )

    # sirf ek monitoring signal present hone ki vjah se
    # investigation honi chahiye.
    assert report["decision"]["action"] == "investigate"