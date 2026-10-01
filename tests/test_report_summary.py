import json
from src.monitoring import report_summary
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

# test verify krta hai ki CLI main function
# latest monitoring summary ko terminal pr display krta hai.
def test_report_summary_main(tmp_path, monkeypatch, capsys):
    # Fake summary kr rhe hai.
    summary = {
        "report_generated_at": "2026-09-30T13:42:18+00:00",
        "model_version": "baseline",
        "reference_dataset": "bank-full.csv",
        "overall_drift": True,
        "drifted_features": 1,
        "overall_performance_degraded": False,
        "action": "investigate",
    }

    # actual report loading ko temporarily replace kr rhe hai.
    monkeypatch.setattr(
        report_summary,
        "get_latest_monitoring_summary",
        lambda: summary,
    )

    # CLI main function run kr rhe hai.
    report_summary.main()

    # terminal output capture kr rhe hai.
    captured = capsys.readouterr()

    # important information output me present honi chahiye.
    assert "DriftGuard Monitoring Summary" in captured.out
    assert "Model version: baseline" in captured.out
    assert "Overall drift: True" in captured.out
    assert "Drifted features: 1" in captured.out
    assert "Performance degraded: False" in captured.out
    assert "Recommended action: investigate" in captured.out