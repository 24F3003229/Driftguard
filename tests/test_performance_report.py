import pytest
from src.monitoring.performance_report import (
    generate_performance_report,
)

# ye test verify krta hai ki performance report
# correctly performance degradation detect kr rhi hai.
def test_generate_performance_report():
    # baseline/reference model performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # current model ki performance define kr rhe hai.
    current_metrics = {
        "accuracy": 0.89,
        "precision": 0.62,
        "recall": 0.28,
        "f1_score": 0.39,
        "roc_auc": 0.88,
    }

    # performance report generate kr rhe hai.
    report = generate_performance_report(
        reference_metrics,
        current_metrics,
        degradation_threshold=0.05,
    )

    # F1-score ka change -0.06 hona chahiye.
    assert report["changes"]["f1_score"] == pytest.approx(-0.06)

    # recall ka change -0.07 hona chahiye.
    assert report["changes"]["recall"] == pytest.approx(-0.07)

    # recall or f1 dono threshold se zyada degrade hue hai.
    assert report["degradation"]["recall"] is True
    assert report["degradation"]["f1_score"] is True

    # accuracy ka decrease sirf 0.01 hai,
    # jo threshold 0.05 se chhota hai.
    assert report["degradation"]["accuracy"] is False

    # overall performance degradation detect honi chahiye.
    assert report["summary"]["overall_performance_degraded"] is True

    # degraded metrics list me recall or f1_score hone chahiye.
    assert report["summary"]["degraded_metrics"] == [
        "recall",
        "f1_score",
    ]

    # report me exact threshold preserve hona chahiye.
    assert report["configuration"]["degradation_threshold"] == 0.05

# ye test verify krta hai ki jab performance degrade nhi hoti,
# report overall degradation False return krti hai.
def test_generate_performance_report_no_degradation():
    # reference performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # current performance same hai.
    current_metrics = reference_metrics.copy()

    # report generate kr rhe hai.
    report = generate_performance_report(
        reference_metrics,
        current_metrics,
    )

    # koi metric degrade nhi hua hai.
    assert report["summary"]["degraded_metrics"] == []

    # overall degradation False honi chahiye.
    assert report["summary"]["overall_performance_degraded"] is False