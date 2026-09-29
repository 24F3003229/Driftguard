import json
import pandas as pd

from src.monitoring.monitoring_pipeline import (
    run_monitoring_pipeline,
)

# ye integration test verify krta hai ki complete monitoring pipeline
# reports generate krke usse JSON file me save bhi krti hai.
def test_run_monitoring_pipeline(tmp_path):
    # reference dataset define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "balance": [100] * 50 + [101] * 50,
    })

    # current dataset reference ke same rakhi hai.
    # isliye data drift nhi hona chahiye.
    current_df = reference_df.copy()

    # reference model performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # current performance same rkhi hai.
    # isliye performance degradation nhi honi chahiye.
    current_metrics = reference_metrics.copy()

    # temporary JSON output path define kr rhe hai.
    output_path = tmp_path / "monitoring_report.json"

    # complete monitoring pipeline run kr rhe hai.
    report = run_monitoring_pipeline(
        reference_df,
        current_df,
        ["age", "balance"],
        [],
        reference_metrics,
        current_metrics,
        output_path,
    )

    # pipeline ko generated report return krni chahiye.
    assert report["decision"]["action"] == "no_action"

    # JSON monitoring reports file create honi chahiye.
    assert output_path.exists()

    # saved JSON reports ko read file kr rhe hai.
    with output_path.open("r", encoding="utf-8") as file:
        saved_report = json.load(file)

    # saved report returned report ke equal honi chahiye.
    assert saved_report == report

# ye integration test verify krta hai ki jab output_path
# provide nhi kiya jata, pipeline automatically report path generate krti hai.
def test_run_monitoring_pipeline_with_automatic_path(
        tmp_path,
        monkeypatch,
):
    # reference dataset define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "balance": [100] * 50 + [101] * 50,
    })

    # current dataset reference ke same rkhi hai.
    current_df = reference_df.copy()

    # reference model performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # current performance same rkhi hai.
    current_metrics = reference_metrics.copy()

    # automatic report path ke liye temporary reports directory 
    # use kr rhe hai taaki actual project reports directory me file na bane.
    reports_directory = tmp_path / "reports"

    # report path generator ko temporary directory use krne ke liye
    # temporariy repalce kr rhe hai.
    monkeypatch.setattr(
        "src.monitoring.monitoring_pipeline.create_report_path",
        lambda: reports_directory / "monitoring_report_test.json",
    )

    # output_path intentionally provide nhi kr rhe hai.
    report = run_monitoring_pipeline(
        reference_df,
        current_df,
        ["age", "balance"],
        [],
        reference_metrics,
        current_metrics,
    )

    # automatically generated report file exit honi chahiye.
    output_path = reports_directory / "monitoring_report_test.json"

    assert output_path.exists()

    # pipeline se returned report no_action honi chahiye.
    assert report["decision"]["action"] == "no_action"