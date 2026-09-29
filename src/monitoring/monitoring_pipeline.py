# existing monitoring report generation function ko import kr rhe hai.
# ye drift, performance or final decision ka report generate krega.
from src.monitoring.monitoring_report import (
    generate_monitoring_report,
)

# existing report storage function kon import kr rhe hai.
# ye generated monitoring report ko JSON file me save krega.
from src.monitoring.report_storage import (
    save_monitoring_report,
)

# ye function complete monitoring workflow ko orchestrate karega.
#
# 1. Monitoring report generate krega.
# 2. Generated report ko JSON file me save krega.
# 3. Generated report return krega.
#
#IMPORTANT:
# ye function khud drift ya performance calculate nhi krta.
# ye existing components ko combine krta hai.
def run_monitoring_pipeline(
        reference_df,
        current_df,
        numeric_columns,
        categorical_columns,
        reference_metrics,
        current_metrics,
        output_path,
        model_version="baseline",
        reference_dataset="bank-full.csv",
        numeric_significance_level=0.05,
        numeric_effect_threshold=0.05,
        categorical_significance_level=0.05,
        retraining_review_ratio=0.5,
        degradation_threshold=0.05,
):
    # complete monitoring report generate kr rhe hai.
    report = generate_monitoring_report(
        reference_df,
        current_df,
        numeric_columns,
        categorical_columns,
        reference_metrics,
        current_metrics,
        model_version=model_version,
        reference_dataset=reference_dataset,
        numeric_significance_level=numeric_significance_level,
        numeric_effect_threshold=numeric_effect_threshold,
        categorical_significance_level=categorical_significance_level,
        retraining_review_ratio=retraining_review_ratio,
        degradation_threshold=degradation_threshold,
    )

    # generated monitoring report ko JSON file me save kr rhe hai.
    save_monitoring_report(
        report,
        output_path,
    )

    # generated report caller ko return kr rhe hai.
    return report