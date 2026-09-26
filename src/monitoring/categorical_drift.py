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

# ye function DataFrame ke selected categorical columns pr
# Chi-square test run krega.
# significance_level parameter se hum decide kr sakte hai
# ki kitne p-value pr categorical drift report karna hai.
def detect_categorical_drift_for_dataframe(
        reference_df,
        current_df,
        categorical_columns,
        significance_level=0.05,
):
    results = {}

    for column in categorical_columns:
        statistic, p_value = detect_categorical_drift(
            reference_df[column],
            current_df[column],
        )

        results[column] = {
            "statistic": statistic,
            "p_value": p_value,

            # har categorical feature ka p-value configured threshold
            # ke against check karke final drift decision le rhe hai.
            "drift_detected": is_categorical_drifted(
                p_value,
                significance_level=significance_level,
            ),
        }

    return results
    

if __name__ == "__main__":
    df = pd.read_csv("data/bank-full.csv", sep=";")

    categorical_columns = [
        "job",
        "marital",
        "education",
        "default",
        "housing",
        "loan",
        "contact",
        "month",
        "poutcome",
    ]

    reference_df = df.copy()

    current_df = df.copy()

    results = detect_categorical_drift_for_dataframe(
        reference_df,
        current_df,
        categorical_columns,
    )

    for column, result in results.items():
        print(f"\nFeature: {column}")
        print("Chi-square statistic:", result["statistic"])
        print("p-value:", result["p_value"])
        print("Drift detected:", result["drift_detected"])
