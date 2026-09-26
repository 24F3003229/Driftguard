from src.monitoring.numeric_drift import (
    # Numeric drift ke liye existing detector, ye har numeric feature
    # ka KS statistic or p-value calculate karega
    detect_numeric_drift_for_dataframe,
)
from src.monitoring.categorical_drift import (
    # categorical drift ke liye existing detector, ye har categorical feauture ka 
    # Chi-square statistic, p-value or decision calculate krega
    detect_categorical_drift_for_dataframe,
)



# ye funciton reference or current data ko lekar numeric or categorical features
# ka drift analysis ek single unified report mein combine karega
def generate_drift_report(
        reference_df,
        current_df,
        numeric_columns,
        categorical_columns,
):
    # Numeric features par already-tested KS drift detector run kar rahe hai.
    # Isse har numeric column ka statistic, p-value or drift decision milega.
    numeric_results = detect_numeric_drift_for_dataframe(
        reference_df,
        current_df,
        numeric_columns,
    )

    # categorical features pr Chi-square based drift detection run kar rhe hai,
    # har categorical feature ka statistic, p-value or drift decision milega.
    categorical_results = detect_categorical_drift_for_dataframe(
        reference_df,
        current_df,
        categorical_columns,
    )

    # numeric or categorical dono ke results ko
    # ek single unified dictionary mein combine kr rhe hai.
    return {
        "numeric": numeric_results,
        "categorical": categorical_results,
    }


# ye block sirf manually unified report ko test krne ke liye hai.
# jab file ko directly run krenge tabhi ye code execute hoga.
if __name__ == "__main__":
    import pandas as pd

    # original dataset ko reference or current data ke liye load kar rhe hai.
    df = pd.read_csv("data/bank-full.csv", sep=";")

    # ye vhi numeric feature hai jin pr hum KS test use kar rhe hai.
    numeric_columns = [
        "age",
        "balance",
        "day",
        "duration",
        "campaign",
        "pdays",
        "previous",
    ]

    # ye categorical features hain jin pr Chi-square drift test run hoga.
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

    # reference data hmara baseline hai, isliye hum is data ko change nnhi krenge
    reference_df = df.copy()

    # current data abhi reference ke same rakha hai,
    # taaki normal/no-drift scenario ko represent kre.
    current_df = df.copy()

    # unified report function ko call karke
    # numeric or categorical dono drift results le rhe hai.
    report = generate_drift_report(
        reference_df,
        current_df,
        numeric_columns,
        categorical_columns,
    )

    print(report)