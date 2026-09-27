# ye function reference/baseline performance or
# current model performance ke bich me metric changes calculate krega.
#
# positive change ka matlab metric improve hua.
# negative change ka matlab metric decrease hua.
def calculate_performance_change(reference_metrics, current_metrics):
    # har metric ka current value or reference value kr rhe hai.
    changes = {}

    # reference or current dono me available metrics pr iterate kr rhe hai.
    for metric in reference_metrics:
        # current metrics me bhi same metric available hai
        # tabhi uska change calculate karenge.
        if metric in current_metrics:
            # current performance se reference performance subtract kr rhe hai.
            #EXAMPLE:
            # reference F1 = 0.45
            # current F1 = 0.39
            # change = -0.06
            changes[metric] = current_metrics[metric] - reference_metrics[metric]

    return changes

# ye function chech krta hai ki ksi performance metric ka
# decreased configured threshold se zyada hai nhi.
#
#EXAMPLE:
# performance_change = -0.06
# defradation_threshold = 0.05
#
# 0.06 >= 0.05 hine ki vjah se  degradation detect hoga.
def is_performance_degraded(
        performance_change,
        degradation_threshold=0.05,
):
    # negative change ka magnitude calculate kr rhe hai.
    # abs() isliye use kr rhe hai kyunki hme decrease ki
    # actual size dekhni hai.
    decrease = abs(performance_change)

    # sirf negative change ko degradation maana jaayega.
    # agr performance improve hui hai, to degradation False rhega.
    return bool(
        performance_change < 0
        and decrease >= degradation_threshold
    )

# ye funciton multiple performance metrics ke changes ko
# ek sath evaluate krega or har metric ka degradation status return krega.
#
#EXAMPLE:
# {
#       "accuracy": False,
#       "precision": False,
#       "recall": True,
#       "f1_score": True,
#       "roc_auc": False
# }
def detect_performance_degradation(
        performance_changes,
        degradation_threshold=0.05,
):
    # har metric ka degradation result store krne ke liye
    # empty dictionary create r rhe hai.
    degradation_results = {}

    # har performance metric ke change pr iterate kr rhe hai.
    for metric, change in performance_changes.items():
        # individual metricke existing degradation logic
        # use kr rhe hai
        degradation_results[metric] = is_performance_degraded(
            change,
            degradation_threshold=degradation_threshold,
        )
    return degradation_results

# ye function multiple metrices ke degradation results ko 
# ek simple overall summary me convert krega.
#
# ISSE HUME PTA CHALEGA:
# 1. Konse metrics degraded hai
# 2. kya overall perforemance degradation detect hue hai.
def summarize_performance_degradation(degradation_results):
    # sirf un metrics ke names collect kr rhe hai
    # jinka degradation status True hai.
    degraded_metrics = [
        metric
        for metric, degraded in degradation_results.items()
        if degraded
    ]

    # agr ek bhi metric degraded hai
    # to overall performance degradation true hogi.
    overall_performance_degraded = len(degraded_metrics) > 0

    return {
        "degraded_metrics": degraded_metrics,
        "overall_performance_degraded": overall_performance_degraded,
    }