import pandas as pd
from scipy.stats import ks_2samp

def detect_numeric_drift(reference, current):
    statistic, p_value = ks_2samp(reference, current)

    return statistic, p_value

def is_numeric_drifted(p_value, significance_level=0.05):
    return p_value < significance_level

def detect_numeric_drift_for_dataframe(
        reference_df,
        current_df,
        numeric_columns,
):
    results = {}

    for column in numeric_columns:
        statistic, p_value = detect_numeric_drift(
            reference_df[column],
            current_df[column],
        )

        results[column] = {
            "statistic": statistic,
            "p_value": p_value,
            "drift_detected": is_numeric_drifted(p_value),
        }

    return results

if __name__ == "__main__":
    df = pd.read_csv("data/bank-full.csv", sep=";")

    numeric_columns = [
        "age",
        "balance",
        "day",
        "duration",
        "campaign",
        "pdays",
        "previous",
    ]

    reference_df = df.copy()

    current_df = df.copy()
    current_df["age"] += 5

    results = detect_numeric_drift_for_dataframe(
        reference_df,
        current_df,
        numeric_columns,
    )

    for column, result in results.items():
        print(
            column,
            "KS statistic:", result["statistic"],
            "p-value:", result["p_value"],
            "drift_detected:", result["drift_detected"],
        )