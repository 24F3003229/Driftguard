import pytest
from src.monitoring.performance_monitor import(
    calculate_performance_change,
    is_performance_degraded,
    detect_performance_degradation,
    summarize_performance_degradation,
)

# ye test verify krta hai ki performance metric ka 
# positive change correctly calculate ho rha hai.
def test_calculate_performance_change_improvement():
    # reference/baseline performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90
    }

    # current model ki performance define kr rhe hai.
    current_metrics = {
        "accuracy": 0.92,
        "precision": 0.66,
        "recall": 0.40,
        "f1_score": 0.50,
        "roc_auc": 0.92,
    }

    # performance changes calculate kr rhe hai.
    changes = calculate_performance_change(
        reference_metrics,
        current_metrics,
    )

    # F1-score 0.45 se 0.50 hua,
    # isliye change +0.05 hona chahiye.
    assert changes["f1_score"] == pytest.approx(0.05)

# ye test verify krta hai ki performance decrease hone pr
# negative change correctly calculate hota hai.
def test_calculate_performance_change_degradation():
    # reference/baseline performance define kr rhe hai.
    reference_metrics = {
        "accuracy": 0.90,
        "precision": 0.64,
        "recall": 0.35,
        "f1_score": 0.45,
        "roc_auc": 0.90
    }

    # current performance me metrics decrease ho rhe hai.
    current_metrics = {
        "accuracy": 0.88,
        "precision": 0.60,
        "recall": 0.30,
        "f1_score": 0.40,
        "roc_auc": 0.87,
    }

    # performace changes calculate kr rhe hai.
    changes = calculate_performance_change(
        reference_metrics,
        current_metrics,
    )

    # F1-score 0.45 se 0.40 hua,
    # isliye change -0.05 hona chahiye
    assert changes["f1_score"] == pytest.approx(-0.05)

# ye test verify krta hai ki small performance decrease ko
# degradation nhi mana ja rha.
def test_performance_degradation_below_threshold():
    # F1-score me sirf 0.02 ka decrease hua hai.
    change = -0.02

    # degradation threshold 0.05 hai.
    degraded = is_performance_degraded(
        change,
        degradation_threshold=0.05,
    )

    # 0.02 < 0.05, isliye degradation False hona chahiye.
    assert degraded is False

# ye test verify krta hai ki sufficiently large 
# performance decrease ko degradation maana ja rha hai.
def test_performance_degradation_above_threshold():
    # F1-score me 0.08 ka decrease hua hai.
    change = -0.08

    # degradation threshold 0.05 hai,
    degraded = is_performance_degraded(
        change,
        degradation_threshold=0.05,
    )

    # 0.08 >= 0.05, isliye degradation True hona chahiye.
    assert degraded is True

# ye test verify krta hai ki performance improve hone pr
# degradation detect nhi hota.
def test_performance_improvement_is_not_degradation():
    # F1-score improve hua hai.
    change = 0.08

    # performance degradation check kr rhe hai
    degraded = is_performance_degraded(
        change,
        degradation_threshold=0.05,
    )

    # positive change improvement ko represent krta hai,
    # isliye degradation False hona chahiye.
    assert degraded is False

# ye test verify krta hai ki degradation threshold
# actual performance degradaiton decision ko control krta hai.
def test_performance_degradation_threshold_changes_decision():
    # performance me 0.06 ka decrease hua hai.
    change = -0.06

    # normal threshold 0.05 ke sath degradation detect hona chahiye.
    degraded = is_performance_degraded(
        change,
        degradation_threshold=0.05,
    )

    # 0.06 >= 0.05, isliye degradation true hona chahiye.
    assert degraded is True

    # ab threshold ko 0.10 kr rhe hai
    # 0.06 is threshold se chhota hai
    strict_degraded = is_performance_degraded(
        change,
        degradation_threshold=0.10,
    )

    # isliye same performance change ko ab degradation nhi mana jayega.
    assert strict_degraded is False

# ye test verify krta hai ki multiple performance metrics
# ko ek saath evaluate kiya ja rha hai.
def test_detect_performance_degradation_multiple_metrics():
    # different performance metrics ke changes define kr rhe hai.
    performance_changes = {
        "accuracy": -0.01,
        "precision": -0.03,
        "recall": -0.08,
        "f1_score": -0.06,
        "roc_auc": -0.01
    }

    # multiple metrices ka degradation status calculate kr rhe hai.
    results = detect_performance_degradation(
        performance_changes,
        degradation_threshold=0.05,
    )

    # accuracy ke decrease threshold se chhota hai
    assert results["accuracy"] is False

    # precision ke decrease threshold se chhota hai
    assert results["precision"] is False

    # recall ke decrease threshold se bda hai.
    assert results["recall"] is True

    # F1-score ke decrease theshold se bda hai.
    assert results["f1_score"] is True

    # ROC-AUC ke decrease threshold se chhota hai.
    assert results["roc_auc"] is False

# ye test verify krta hai ki degraded metrics correctly
# summary me identify ho rha hain.
def test_summarize_performance_degradation():
    # different metrics ke degradation results define kr rhe hai.
    degradation_results = {
        "accuracy": False,
        "precision": False,
        "recall": True,
        "f1_score": True,
        "roc_auc": False,
    }

    # performance degradation summary generate kr rhe hai.
    summary = summarize_performance_degradation(
        degradation_results,
    )

    # sirf recall  or f1_score degraded hone chahiye.
    assert summary["degraded_metrics"] ==["recall", "f1_score",]

    # at least one metrics degraded hai,
    # isliye overall degradation True honi chahiye.
    assert summary["overall_performance_degraded"] is True

# ye test verify krta hai ki jab koi metric degraded nhi hai,
# overall performance degradation False hoti hai.
def test_summarize_performance_no_degradation():
    # kisi bhi metric me degradation nhi hai
    degradation_results = {
        "accuracy": False,
        "precision": False,
        "recall": False,
        "f1_score": False,
        "roc_auc": False,
    }

    # summary generate kr rhe hai.
    summary = summarize_performance_degradation(
        degradation_results
    )

    # koi degraded metric nhi hona chahiye.
    assert summary["degraded_metrics"] == []

    # isliye overall degradation bhi False honi chahiye.
    assert summary["overall_performance_degraded"] is False