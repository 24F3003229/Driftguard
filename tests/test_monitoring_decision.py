# monitoring decision function ko import kr rhe hai.
from src.monitoring.monitoring_decision import (
    determine_monitoring_action,
)

# ye test verify krta hai ki jab drift or performance 
# dono normal hao to koi action recommend nhi hota.
def test_monitoring_action_no_action():
    # dono moitoring signals healthy hai.
    action = determine_monitoring_action(
        overall_drift=False,
        overall_performance_degraded=False,
    )

    # expected action no_action hai.
    assert action == "no_action"

# ye test verify krta hai ki sirf data drift hone pr
# investigation recommend hoti hai.
def test_monitoring_action_drift_only():
    # data drift hai, lekin model performance degraded nhi hai.
    action = determine_monitoring_action(
        overall_drift=True,
        overall_performance_degraded=False,
    )

    # sirf ek signal hone ki vjah se investigation krenge.
    assert action == "investigate"

# ye test verify krta hai ki sirf performance degradation
# hone pr investigation recommend hoti hai.
def test_monitoring_action_performance_only():
    # data drift nhi hai, lekin model performance degraded hai.
    action = determine_monitoring_action(
        overall_drift=False,
        overall_performance_degraded=True,
    )

    # sirf performance problem hone pr investigation krenge.
    assert action == "investigate"

# ye test verify krta hai ki jab data drift or performance
# degradation dono present ho to retraining evaluate ki jaati hai.
def test_monitoring_action_drift_and_performance():
    # dono monitoring signals preblematic hai.
    action = determine_monitoring_action(
        overall_drift=True,
        overall_performance_degraded=True,
    )

    # dono signals ek sath hone pr retraining evaluation recommend hogi.
    assert action == "evaluate_retraining"