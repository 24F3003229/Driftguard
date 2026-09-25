from src.monitoring.categorical_drift import detect_categorical_drift

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