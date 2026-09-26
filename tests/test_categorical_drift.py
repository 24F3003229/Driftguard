import pandas as pd
from src.monitoring.categorical_drift import (
    detect_categorical_drift,
    is_categorical_drifted,
    detect_categorical_drift_for_dataframe,
)

def test_no_categorical_drift():
    reference = ["A", "B", "A", "B", "C"]
    current = ["A", 'B', "A", "B", "C"] 

    statistic, p_value = detect_categorical_drift(
        reference,
        current,
    )

    assert statistic == 0.0
    assert p_value == 1.0

def test_categorical_drift():
    reference = (
        ["A"] * 500
        + ["B"] * 500
    )

    current = (
        ["A"] * 200
        + ["B"] * 800
    )

    statistic, p_value = detect_categorical_drift(
        reference,
        current,
    )

    assert statistic > 0.0
    assert p_value < 0.05

def test_new_category_in_current_data():
    reference = ["A"] * 500 + ["B"] * 500
    current = ["A"] * 450 + ["B"] * 450 + ["C"] * 100

    statistic, p_value = detect_categorical_drift(
        reference, 
        current,
    )

    assert statistic > 0.0
    assert p_value < 0.05

def test_categorical_drift_decision():
    assert is_categorical_drifted(0.01) is True
    assert is_categorical_drifted(0.10) is False

def test_categorical_drift_boundary():
    assert is_categorical_drifted(0.05) is False

def test_categorical_drift_for_dataframe():
    reference_df = pd.DataFrame({
        "job": ["A"] * 500 + ["B"] * 500,
        "marital": ["X"] * 500 + ["Y"] * 500,
    })

    current_df = pd.DataFrame({
        "job": ["A"] * 200 + ["B"] * 800,
        "marital": ["X"] * 500 + ["Y"] * 500,
    })

    results = detect_categorical_drift_for_dataframe(
        reference_df,
        current_df,
        ["job", "marital"],
    )

    assert results["job"]["drift_detected"] is True
    assert results["marital"]["drift_detected"] is False