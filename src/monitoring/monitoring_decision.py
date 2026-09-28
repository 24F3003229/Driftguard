# ye function data drift or model performance degradation
# ko combine krke overall monitoring action decide krega.
# 
#IMPORTANT:
# ye fucntion automatic retraining nhi krta
# ye sirf monitoring recommendation generate krta hai.
def determine_monitoring_action(
    overall_drift,
    overall_performance_degraded,
):
    # agr data drift or performance degradation dono nhi hai,
    # to immediate action ki zrurat nhi hai.
    if not overall_drift and not overall_performance_degraded:
        return "no_action"

    # agr dono signals simultaneously present hai,
    # to retraining evaluation comsider krni chahiye.
    if overall_drift and overall_performance_degraded:
        return "evaluate_retraining"

    # agr sirf ek signal present hai,
    # to pehle investigation krni chahiye.
    return "investigate"