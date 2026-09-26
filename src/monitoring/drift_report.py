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

    # reference dataset me ktine observations hai, 
    # uska count report me store kr rhe hai.
    reference_samples = len(reference_df)

    # current dataset me kitne observations hai,
    # uska count report me store kr rhe hai.
    current_samples = len(current_df)
    
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

    # numeric or categorical dono results ko ek jagah combine kr rhe hai
    # taki total monitored features count kr ske.
    all_results = {
        **numeric_results,
        **categorical_results,
    }


    # har feature ke result me drift_detected True/False hota hai
    # sirf True wale features ko count kr kre hai.
    drifted_features = sum(
        result["drift_detected"]
        for result in all_results.values()
    )

    # total monitored features numeric + categorical features ka count hai.
    total_features = len(all_results)

    # agr ek bhi feature drifted hai, to overall drift status True hoga.
    overall_drift = drifted_features > 0 

    # final report me summary, dataset size or detailed feature-level preserve kr rhe hai.
    return {
        "summary": {
            "total_features": total_features,
            "drifted_features": drifted_features,
            "overall_drift": overall_drift,
        },
        "metadata": {
            "reference_samples": reference_samples,
            "current_samples": current_samples,
        },
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

    # reference data hmara baseline hai, isliye hum is data ko change nhi krenge
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