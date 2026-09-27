# Existing performance monitoring functions ko import kr rhe hai.
# in functions ko reuse  krenge intead of same logic dobara likhne ke.
from src.monitoring.performance_monitor import (
    calculate_performance_change,
    detect_performance_degradation,
    summarize_performance_degradation,
)

# ye function reference or current model metrics ko 
# ek complete performance monitoring report me combine krega.
#
#IS REPORT ME:
# 1. performace changes
# 2. metric-wise degradation
# 3. overall degradation
# 4. configuration
# store ki jayegi
def generate_performance_report(
        reference_metrics,
        current_metrics,
        degradation_threshold=0.05,
):
    # reference or current metrics ke bich
    # actual performance changes calculate kr rhe hai.
    performance_changes = calculate_performance_change(
        reference_metrics,
        current_metrics,
    )

    # har metric ke performance change ko configured
    # degradation threshold ke against check kr rhe hai.
    degradation_results = detect_performance_degradation(
        performance_changes,
        degradation_threshold=degradation_threshold,
    )

    # metric-wise degradation results ko
    # overall performance summary me convert kr rhe hai.
    summary = summarize_performance_degradation(
        degradation_results,
    )

    # saare results ko ek single structured report me 
    # combine krke return kr rhe hai.
    return {
        "summary": summary,
        "reference_metrics": reference_metrics,
        "current_metrics": current_metrics,
        "changes": performance_changes,
        "degradation": degradation_results,
        "configuration": {
            "degradation_threshold": degradation_threshold,
        }
    }

# ye block sirf module ko directly run krne pr
# example performance report generate krke print krega.
if __name__ == "__main__":
    # baseline model ke example/reference performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.9012,
        "precision": 0.6445,
        "recall": 0.3478,
        "f1_score": 0.4518,
        "roc_auc": 0.9056,
    }

    # current model ki simulated performance define kr rhe hai.
    # ye real profuction data nhi hai; sirf monitoring logic test krne ke liye hai.
    current_metrics = {
        "accuracy": 0.8912,
        "precision": 0.6245,
        "recall": 0.2878,
        "f1_score": 0.3918,
        "roc_auc": 0.8856,
    }

    # performance report generate kr rhe hai.
    report = generate_performance_report(
        reference_metrics,
        current_metrics,
    )

    # complete performance report print kr rhe hai.
    print(report)