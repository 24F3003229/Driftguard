import json
from src.monitoring.report_summary import (
    get_latest_monitoring_summary,
)

# ye test verify krta hai ki latest monitoring report se 
# required summary information correctly extract ho rhi hai.
def test_get_latest_monitoring_summary(tmp_path):
    # test ke liye monitoring report define kr rhe hai.
    report = {
        "metadata": {
            "report_generated_at": "2026-09-30T13:42:18+00:00",
            "model_version": "baseline",
            "reference_dataset": "bank-full.csv",
        },
        "drift": {
            "summary": {
                "total_features": 16,
                "drifted_features": 1,
                "overall_drift": True,
                "action": "investigate",
            },
        },
        "performance": {
            "summary": {
                "overall_performance_degraded": False,
            },
        },
        "decision": {
            "action": "investigate",
        },
    }

    # temporary reports directory create kr rhe hai.
    reports_directory = tmp_path / "reports"
    reports_directory.mkdir()

    # test report JSON file me save kr rhe hai.
    report_path = reports_directory / "monitoring_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file)

    # latest report ka summary generate kr rhe hai.
    summary = get_latest_monitoring_summary(reports_directory)

    # important fields verify kr rhe hai.
    assert summary["model_version"] == "baseline"
    assert summary["overall_drift"] is True
    assert summary["drifted_features"] == 1
    assert summary["overall_performance_degraded"] is False
    assert summary["action"] == "investigate"