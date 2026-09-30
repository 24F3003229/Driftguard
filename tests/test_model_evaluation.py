import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression

from src.monitoring.model_evaluation import (
    evaluate_model,
    evaluate_baseline_model_on_datasets,
    evaluate_baseline_model_with_performance_report,
)

# ye test verify krta hai ki evaluate_model
# required classification metrics correctly return krta hai.
def test_evaluate_model():
    # simple binary classification dataset create kr rhe hai.
    X = pd.DataFrame({
        "feature": [
            0,1,2,3,4,
            5,6,7,8,9,
        ],
    })

    # corresponding binary labels define kr rhe hai.
    y = pd.Series([
        0,0,0,0,0,
        1,1,1,1,1,
    ])

    # test ke liye simple Logistic Regression model create kr rhe hai.
    model = LogisticRegression()

    # model ko test dataset pr train kr rhe hai.
    model.fit(X, y)

    # trained model ki metrics calculate kr rhe hai.
    metrics = evaluate_model(model, X, y)

    # expected metrics report me available honi chahiye.
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_auc" in metrics

    # har metric valid probability-like range
    # 0 se 1 ke bich honi chahiyee.
    for value in metrics.values():
        assert 0.0 <= value <= 1.0

def test_evaluate_baseline_model_on_datasets(tmp_path):
    # small training dataset create kr rhe hai.
    # taaki temporary model bana ske.
    X_train = pd.DataFrame({
        "feature": [0, 1, 2, 3, 4, 5],
    })

    y_train = pd.Series([0, 0, 0, 1, 1, 1])

    # simple Logistic Regression model train kr rhe hai.
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # temporary model file create kr rhe hai.
    model_path = tmp_path / "model.joblib"
    joblib.dump(model, model_path)

    # reference or current datasets same rakhe hai.
    # is test ka purpose function ka integration verify krna hai.
    reference_df = X_train.copy()
    current_df = X_train.copy()

    y = y_train.copy()

    # saved model ko load krke dono datasets pr evaluation kr rhe hai.
    reference_metrics , current_metrics = (
        evaluate_baseline_model_on_datasets(
            model_path,
            reference_df,
            current_df,
            y,
        )
    )

    # dono metric dictionaries contain hone chahiye.
    assert isinstance(reference_metrics, dict)
    assert isinstance(current_metrics, dict)

    # required metrics available hone chahiye.
    for metrics in [reference_metrics, current_metrics]:
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        assert "roc_auc" in metrics

def test_evaluate_baseline_model_with_performance_report(tmp_path):
    # small dataset create kr rhe hai.
    X_train = pd.DataFrame({
        "feature": [0, 1, 2, 3, 4, 5],
    })

    y_train = pd.Series([0, 0, 0, 1, 1, 1])

    # temporary Logistic Regression model train kr rhe hai.
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # model ko temporary file me save kr rhe hai.
    model_path = tmp_path / "model.joblib"
    joblib.dump(model, model_path)

    # same data ko reference or current ke liye use kr rhe hai.
    reference_df = X_train.copy()
    current_df = X_train.copy()

    # model evaluation + performance report run kr rhe hai.
    result = evaluate_baseline_model_with_performance_report(
        model_path,
        reference_df,
        current_df,
        y_train,
    )

    # result me required sections hone chahiye.
    assert "reference_metrics" in result
    assert "current_metrics" in result
    assert "performance_report" in result

    # same data use hua hai, isliye performance degradation nhi honi chahiye.
    assert (
        result["performance_report"]["summary"]["overall_performance_degraded"] is False
    )