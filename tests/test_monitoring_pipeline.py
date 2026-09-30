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

# ye integration test verify krta hai ki agr data drift detect ho
# lekin model performance degrade na ho, to action "investigate" ho.
def test_run_monitoring_pipeline_with_drift_but_stable_performance(tmp_path):
    # reference dataset define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 100,
        "balance": [100] * 100,
    })

    # current dataset me age distribution intentionally change kr rhe hai.
    # isse numeric drift detect honi chaiye.
    current_df = pd.DataFrame({
        "age": [30] * 100,
        "balance": [100] * 100,
    })

    # reference model performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # performance same rakhi hai.
    # isliye performance degradation nhi honi chahiye.
    current_metrics = reference_metrics.copy()

    # temporary report path define kr rhe hai.
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

    # age distribution change ki vjah se drift detect honi chahiye.
    assert report["drift"]["summary"]["overall_drift"] is True

    # performance stable hone ki vjah se degradation nhi honi chahiye.
    assert (
        report["performance"]["summary"]["overall_performance_degraded"] is False
    )

    # sirf drift hone pr monitoring action investigate hona chahiye.
    assert report["decision"]["action"] == "investigate"

    # monitoring report JSON file me save honi chahiye
    assert output_path.exists()

# ye integration test verify krta hai ki agr data drift nhi hai 
# lekin model performance degrade ho rhi hai,
# to action "investigate" hona chahiye.
def test_run_monitoring_pipeline_with_performance_degradation(tmp_path):
    # reference dataset define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 100,
        "balance": [100] * 100,
    })

    # current dataset same rakhi hai.
    # isliye data drift detect nhi honi chahiye.
    current_df = reference_df.copy()

    # reference performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90,
    }

    # recall or F1 ko threshold se zyada decrease kr rhe hai.
    # isse performance degradation detect honi chahiye.
    current_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.25,
        "f1_score": 0.35,
        "roc_auc": 0.90,
    }

    # temporary report path define kr rhe hai.
    output_path = tmp_path / "monitoring_report.json"

    # complete monitoring pipeline run kr rhe hai.
    report = run_monitoring_pipeline(
        reference_df,
        current_df,
        ["age", "balance"],
        [],
        reference_metrics,
        current_metrics,
        output_path
    )

    # data same hone ki vjah se drift nhi honi chahiye.
    assert report["drift"]["summary"]["overall_drift"] is False

    # recall or F1 degrade hue hai.
    assert (
        report["performance"]["summary"]["overall_performance_degraded"] is True
    )

    # sirf performance degradation hone pr investigation honi chahiye.
    assert report["decision"]["action"] == "investigate"

    # monitoring report save honi chahiye.
    assert output_path.exists()