import json
import os
from src.monitoring.report_storage import (
    save_monitoring_report,
    load_monitoring_report,
    load_latest_monitoring_report,
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

# ye test verify krta hai ki saved monitoring report ko 
# JSON file se correctly load kiya ja rha sakta hai.
def test_load_monitoring_report(tmp_path):
    # ek sample monitoring report create kr rhe hai.
    report = {
        "metadata": {
            "model_version": "baseline",
        },
        "decision": {
            "action": "investigate"
        },
    }

    # tempporary JSON file paath create kr rhe hai.
    output_path = tmp_path / "monitoring_report.json"

    # pehle report save kr rhe hai.
    save_monitoring_report(report, output_path)

    # saved report ko JSON file se load kr rhe hai.
    loaded_report = load_monitoring_report(output_path)

    # loaded report original report ke equal honi chahiye
    assert loaded_report == report

# ye test verify krta hai ki reports directory me 
# latest monitoring report correctly identify ho rhi hai.
def test_load_latest_monitoring_report(tmp_path):
    # first monitoring report create kr rhe hai.
    first_report = {
        "metadata": {
            "model_version": "baseline",
        },
        "decision": {
            "action": "no_action",
        },
    }

    # second monitoring report create kr rhe hai.
    latest_report = {
        "metadata": {
            "model_version": "v2",
        },
        "decision": {
            "action": "investigate",
        },
    }

    # dono reports ko temporary directory me save kr rhe hai.
    first_path = tmp_path / "monitoring_report_1.json"
    latest_path = tmp_path / "monitoring_report_2.json"

    # dono reports ko save kr rhe hai.
    save_monitoring_report(first_report, first_path)
    save_monitoring_report(latest_report, latest_path)

    # first report ka modification time explicitly older set kr rhe hai,
    os.utime(first_path, (1000, 1000))

    # second report ka modification time explicitly newer se kr rhe hai.
    os.utime(latest_path, (2000, 2000))

    # latest report load kr rhe hai.
    loaded_report = load_latest_monitoring_report(tmp_path)

    # latest saved report return honi chahiye.
    assert loaded_report == latest_report