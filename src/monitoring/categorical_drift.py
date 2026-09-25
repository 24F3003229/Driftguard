import pandas as pd
from scipy.stats import chi2_contingency

def detect_categorical_drift(reference, current):
    reference = pd.Series(reference)
    current = pd.Series(current)

    reference_counts = reference.value_counts()
    current_counts = current.value_counts()

    categories = sorted(
        set(reference_counts.index) | set(current_counts.index)
    )

    reference_values = [
        reference_counts.get(category, 0)
        for category in categories
    ]

    current_values = [
        current_counts.get(category, 0)
        for category in categories
    ]

    table = [
        reference_values,
        current_values
    ]

    statistic, p_value, _, _ = chi2_contingency(table)

    return statistic, p_value

def is_categorical_drifted(
        p_value,
        significance_level=0.05,
):
    return bool(
        p_value < significance_level
    )
    

if __name__ == "__main__":
    df = pd.read_csv("data/bank-full.csv", sep=";")

    reference = df["job"]
    current = df["job"].replace({
        "blue-collar": "management",
    })

    statistic, p_value = detect_categorical_drift(
        reference,
        current,
    )

    print("Featues: job")
    print("Chi-square statistic:", statistic)
    print("p-value:", p_value)
