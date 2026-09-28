# Existing drift report function ko import kr rhe hai.
# ye data drift ka complete report generate krega
from src.monitoring.drift_report import (
    generate_drift_report,
)

# Existing performance report function ko import kr rhe hai.
# ye model performance ka complete report generate krega.
from src.monitoring.performance_report import (
    generate_performance_report,
)

# existing monitoring decision function ko import kr rhe hai.
# ye drift or performance signals ko combine krke
# final monitoring action decide krega.
from src.monitoring.monitoring_decision import (
    determine_monitoring_action,
)

# ye function data drift or model performance reports ko 
# ke single unified monitoring report me combine krega.
#
#IS FUNCTION KA MAIN PURPOSE ORCHESTRATION HAI:
# 1. Drift report generate krna
# 2. Performance report generate krna
# 3. Dono results ko monitoring decision me dena
# 4. Final unified report return krna
def generate_monitoring_report(
        reference_df,
        current_df,
        numeric_columns,
        categorical_columns,
        reference_metrics,
        current_metrics,
        numeric_significance_level=0.05,
        numeric_effect_threshold=0.05,
        categorical_significance_level=0.05,
        retraining_review_ratio=0.5,
        degradation_threshold=0.05,
):
    # reference or current data ka complete drift report generate kar rhe hai.
    drift_report = generate_drift_report(
        reference_df,
        current_df,
        numeric_columns,
        categorical_columns,
        numeric_significance_level=numeric_significance_level,
        numeric_effect_threshold=numeric_effect_threshold,
        categorical_significance_level=categorical_significance_level,
        retraining_review_ratio=retraining_review_ratio,
    )

    # reference or current model metrics ka
    # complete performance report generate kr rhe hai.
    performance_report = generate_performance_report(
        reference_metrics,
        current_metrics,
        degradation_threshold=degradation_threshold,
    )

    # drift report se overall data drift status nikal rhe hai.
    overall_drift = drift_report["summary"]["overall_drift"]

    # performance report se overall performance degradation status nikal rhe hai.
    overall_performance_degraded = (
        performance_report["summary"]["overall_performance_degraded"]
    )

    # data drift or performance degradation ko combine krke
    # final monitoring action decide kr rhe hai.
    action = determine_monitoring_action(
        overall_drift=overall_drift,
        overall_performance_degraded=overall_performance_degraded,
    )

    # drift report, performance report pr final decision ko
    # ek single structured monitoring report me combine kr rhe hai.
    return {
        "drift": drift_report,
        "performance":performance_report,
        "decision": {
            "action": action,
        }
    }