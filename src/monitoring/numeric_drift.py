import pandas as pd
from scipy.stats import ks_2samp

def detect_numeric_drift(reference, current):
    statistic, p_value = ks_2samp(reference, current)

    return statistic, p_value

if __name__ == "__main__":
    df = pd.read_csv("data/bank-full.csv", sep=";")

    reference = df["age"]
    current = df["age"]

    statistic, p_value = detect_numeric_drift(
        reference,
        current
    )

    print("Feature: age")
    print("KS statistics:", statistic)
    print("p-value:", p_value)