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

    # unified monitoring report generate kr rhe hai.
    report = generate_monitoring_report(
        reference_df,
        current_df,
        ["age", "balance", "day", "campaign"],
        [],
        reference_metrics,
        current_metrics,
    )

    # unified report me metadata section available hona chahiye.
    assert "metadata" in report

    # report generation timestamp metadata me available hona chahiye
    assert "report_generated_at" in report["metadata"]

    # timestamp empty nhi hona chahiye.
    assert report["metadata"]["report_generated_at"]

    # report me baseline model ka verison record hona chahiye.
    assert report["metadata"]["model_version"] == "baseline"

    # report me reference dataset ka naam record hona chahiye.
    assert report["metadata"]["reference_dataset"] == "bank-full.csv"

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

# ye test verify krta hai ki custom model version or
# reference dataset report metadata me correctly store hote hai.
def test_generate_monitoring_report_custom_metadata():
    # reference dataset create kr rhe hai.
    reference_df = pd.DataFrame({
    "age": [20, 21, 22, 23],
    })

    # current dataset same rakhenge taaki drift na ho.
    current_df = reference_df.copy()

    # reference model metrics define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
    }

    # current model metrics same rkhenge
    current_metrics = reference_metrics.copy()

    # custom model version or dataset identifier pass kr rhe hai.
    report = generate_monitoring_report(
        reference_df,
        current_df,
        ["age"],
        [],
        reference_metrics,
        current_metrics,
        model_version="v2",
        reference_dataset="reference_2026_09",
    )

    # custom model version metadata me correctly store hona chahiye.
    assert report["metadata"]["model_version"] == "v2"

    # custom reference dataset identifier correctly store hona chahiye.
    assert (
        report["metadata"]["reference_dataset"] == "reference_2026_09"
    )