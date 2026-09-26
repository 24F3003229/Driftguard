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


# ye function drifted features ki quantity ke basis pr 
# monitoring system ke liye next action decide krega.

# IMPORTANT:
# drift detect hone ka matlab automatically model retrain nhi krna hai
# pehle investigation or model performance evaluation krna hoga.
def determine_drift_action(
        drifted_features,
        total_features,
        retraining_review_ratio=0.5,
):
    # agr koi bhi feature drift nhi hua,
    # to immediate action ki zrurat nhi hai.
    if drifted_features == 0:
        return "no_action"

    # drifted features ka proportion calculate kar rhe hai.
    drift_ratio = drifted_features / total_features

    # agr monitored features ka sufficiently large portion drifted hai,
    # to retraining ko evaluate krne ka signal denge.
    if drift_ratio >= retraining_review_ratio:
        return "evaluate_retraining"

    # limited drift ke case me pehle investigation krenge.
    return "investigate"

# ye funciton reference or current data ke drift results ko ek single unified report mein combine karega.
# thresholds ko parameter ke through receive karega taaki 
# monitoring decision clearly configurable or reproducible rhe.
def generate_drift_report(
        reference_df,
        current_df,
        numeric_columns,
        categorical_columns,
        numeric_significance_level=0.05,
        numeric_effect_threshold=0.05,
        categorical_significance_level=0.05,
):

    # reference dataset me ktine observations hai, 
    # uska count report me store kr rhe hai.
    reference_samples = len(reference_df)

    # current dataset me kitne observations hai,
    # uska count report me store kr rhe hai.
    current_samples = len(current_df)
    
    # Numeric drift detector ko configured thresholds pass kr kre hai 
    # taaki report or actual decision same configuration use kre.
    numeric_results = detect_numeric_drift_for_dataframe(
        reference_df,
        current_df,
        numeric_columns,
        significance_level=numeric_significance_level,
        effect_threshold=numeric_effect_threshold,
    )

    # report se categorical significance threshold detector ko
    # pass kr rhe hai, taaki actual decision isi value pr based ho.
    categorical_results = detect_categorical_drift_for_dataframe(
        reference_df,
        current_df,
        categorical_columns,
        significance_level=categorical_significance_level,
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

    # drifted features ki quantity or total monitored features
    # ke basis pr next monitoring action decide kar rhe hai.
    action = determine_drift_action(
        drifted_features=drifted_features,
        total_features=total_features,
    )

    # report me vo exact thresholds bhi store kr rhe hai
    # jo drift decision lene ke liye use hue hai.
    # isse report reproducible or easy-to-audit banegi.
    return {
        "summary": {
            "total_features": total_features,
            "drifted_features": drifted_features,
            "overall_drift": overall_drift,
            "action": action,
        },
        "metadata": {
            "reference_samples": reference_samples,
            "current_samples": current_samples,
        },
        "configuration":{
            "numeric_significance_level": numeric_significance_level,
            "numeric_effect_threshold": numeric_effect_threshold,
            "categorical_significance_level": categorical_significance_level,
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