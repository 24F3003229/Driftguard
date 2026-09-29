import json
from src.monitoring.report_storage import (
    save_monitoring_report,
)

# ye test verify krta hai ki monitoring report
# correctly JSON file me save ho rhi hai.
def test_save_monitoring_report(tmp_path):
    # ek small sample monitoring report create kr rhe hai.
    report = {
        "metadata": {
            "model_version": "baseline",
        },
        "decision": {
            "action": "no_action",
        },
    }

    # pytest ka temporary directory use kr rhe hai.
    output_path = tmp_path / "monitoring_report.json"

    # report ko JSON file me save kr rhe hai.
    save_monitoring_report(report, output_path)

    # JSON file successfully create honi chahiye.
    assert output_path.exists()

    # saved JSON file ko read kr rhe hai.
    with output_path.open("r", encoding="utf-8") as file:
        saved_report = json.load(file)

    # saved report original report ke equal honi chahiye.
    assert saved_report == report