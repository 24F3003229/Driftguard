from src.monitoring.numeric_drift import detect_numeric_drift

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