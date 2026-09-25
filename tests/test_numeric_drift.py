from src.monitoring.numeric_drift import (
    detect_numeric_drift,
    detect_numeric_drift_for_dataframe,
    is_numeric_drifted,
)

def test_no_drift():
    reference = [20, 25, 30, 35, 40]
    current = [20, 25, 30, 35, 40]

    statistic, p_value = detect_numeric_drift(
        reference,
        current,
    )

    assert statistic == 0.0
    assert p_value == 1.0


def test_drift():
    reference = list(range(100))
    current = list(range(50,150))

    statistic, p_value = detect_numeric_drift(
        reference,
        current,
    )

    assert statistic > 0.0
    assert p_value < 0.05

def test_multiple_numeric_features():
    import pandas as pd

    reference = pd.DataFrame({
        "age": [20, 25, 30, 35, 40],
        "balance": [100, 200, 300, 400, 500],
    })

    current = pd.DataFrame({
        "age": [70, 75, 80, 85, 90],
        "balance": [100,200, 300, 400, 500],
    })

    results = detect_numeric_drift_for_dataframe(
        reference,
        current,
        ["age", "balance"],
    )

    assert results["age"]["statistic"] > 0.0
    assert results["age"]["p_value"] < 0.05

    assert results["balance"]["statistic"] == 0.0
    assert results["balance"]["p_value"] == 1.0

def test_drift_decision():
    assert is_numeric_drifted(0.01) is True
    assert is_numeric_drifted(0.10) is False

def test_drift_decision_boundary():
    assert is_numeric_drifted(0.05) is False