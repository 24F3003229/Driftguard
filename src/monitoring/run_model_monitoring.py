from src.monitoring.monitoring_report import (
    generate_monitoring_report,
)
from src.monitoring.report_storage import save_monitoring_report
from src.monitoring.report_path import create_report_path
from src.data.monitoring_data import prepare_monitoring_datasets
from src.monitoring.model_evaluation import (
    evaluate_baseline_model_on_datasets,
)

# ye script actual bank marketing dataset ko monitoring 
# ke liye prepare krega or baseline model evaluate krega
def main():
    # actual dataset se reference or current monitoring
    # dataset prepare kr rhe hai.
    (
        reference_df,
        reference_evaluation_df,
        current_df,
        y_test,
    ) = prepare_monitoring_datasets(
        data_path="data/bank-full.csv",
        current_age_shift=5,
    )

    # Monitoring dataset ke numeric or categorical features define kr rhe hai.
    numeric_columns = [
        "age",
        "balance",
        "day",
        "duration",
        "campaign",
        "pdays",
        "previous",
    ]

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

    # saved baseline model ko load krke
    # reference or current evaluation datasets pr metrics calculate kr rhe hai.
    reference_metrics, current_metrics = (
        evaluate_baseline_model_on_datasets(
            model_path="artifacts/baseline_model.joblib",
            reference_df=reference_evaluation_df,
            current_df=current_df,
            y=y_test,
        )
    )

    # drift, performance or monitoring decision ko
    # ek single unified report me combine kr rhe hai.
    monitoring_report = generate_monitoring_report(
        reference_df=reference_df,
        current_df=current_df,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        reference_metrics=reference_metrics,
        current_metrics=current_metrics,
        model_version="baseline",
        reference_dataset="bank-full.csv",
    )

    # har monitoring run ke liye unque timestamp-based
    # report path create kr rhe hai.
    report_path = create_report_path()

    # complete monitoring report ko JSON file me save kr rhe hai.
    save_monitoring_report(
        monitoring_report,
        report_path,
    )

    # saved report ka path print kr rhe hai.
    print("\nMonitoring report saved to:")
    print(report_path)

    # Unified report se drift summary print kr rhe hai.
    print("\nDrift summary:")
    print(monitoring_report["drift"]["summary"])

    # Unified report se final monitoring action print kr rhe hai.
    print("\nMonitoring action:")
    print(monitoring_report["decision"]["action"])

    # Unified report se reference performance print kr rhe hai.
    print("\nReference metrics:")
    print(monitoring_report["performance"]["reference_metrics"])

    # Unified report se current performance print kr rhe hai.
    print("\nCurrent metrics:")
    print(monitoring_report["performance"]["current_metrics"])

    # Unified report se performance analysis print kr rhe hai.
    print("\nPerformance report:")
    print(monitoring_report["performance"])

if __name__=="__main__":
    main()