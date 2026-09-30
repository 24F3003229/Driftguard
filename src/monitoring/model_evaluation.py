import joblib
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

# ye function saved baseline model ko disk se load krega.
def load_baseline_model(
    model_path="artifacts/baseline_model.joblib",
):
    # complete trained sklearn pipeline load kr rhe hai.
    # isme preprocessing pr logistic Regression dono include hai.
    model = joblib.load(model_path)

    # loaded model return kr rhe hai
    return model

# ye function kisi labeled dataset pr model ki
# classification performance metrics calculate krega.
def evaluate_model(model, X, y):
    # model se final class prediction generate kr rhe hai.
    y_pred = model.predict(X)

    # positive class yanai class 1 ki probability nikal rhe hai.
    # ROC-AUC calculate krne ke liye probability required hoti hai.
    y_probability = model.predict_proba(X)[:, 1]

    # important classification metrics calculate kr rhe hai.
    metrics = {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred),
        "recall": recall_score(y, y_pred),
        "f1_score":f1_score(y, y_pred),
        "roc_auc": roc_auc_score(y, y_probability),
    }

    # structured metrics dictionary return kr rhe hai.
    return metrics

def evaluate_baseline_model_on_datasets(
    model_path,
    reference_df,
    current_df,
    y,
):
    # saved baseline model ko disk se load kr rhe hai.
    model = load_baseline_model(model_path)

    # same baseline model se reference dataset ki performance
    # calculate kr rhe hai.
    reference_metrics = evaluate_model(
        model,
        reference_df,
        y,
    )

    # same baseline model se current dataset ki performance
    # calculate kr rhe hai.
    current_metrics = evaluate_model(
        model,
        current_df,
        y,
    )

    # dono performance results ko ek saath return kr rhe hai.
    return reference_metrics, current_metrics

def evaluate_baseline_model_with_performance_report(
    model_path,
    reference_df,
    current_df,
    y,
    degradation_threshold=0.05,
):
    # saved baseline model ko reference or current
    # dono datasets pr evaluate kr rhe hai.
    reference_metrics, current_metrics = (
        evaluate_baseline_model_on_datasets(
            model_path,
            reference_df,
            current_df,
            y,
        )
    )

    # reference or current metrics ko existing
    # performance monitoring logic me bhej rhe hai.
    from src.monitoring.performance_report import (
        generate_performance_report,
    )

    performance_report = generate_performance_report(
        reference_metrics,
        current_metrics,
        degradation_threshold=degradation_threshold,
    )

    # metrics or performance analysis dono return kr rhe hai.
    return {
        "reference_metrics": reference_metrics,
        "current_metrics": current_metrics,
        "performance_report": performance_report,
    }