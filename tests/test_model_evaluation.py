import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.monitoring.model_evaluation import (
    evaluate_model,
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