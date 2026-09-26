import pandas as pd

from src.monitoring.drift_report import (
    generate_drift_report,
    determine_drift_action,
)


# ye test check krta hia ki unified report numeric or categorical dono ka drift
# ek sath correctly detect kr skti hai.
def test_generate_drift_report():
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "job": ["A"] * 50 + ["B"] * 50
    })

    current_df = pd.DataFrame({
        "age": [40] * 50 + [41] * 50, 
        "job": ["A"] * 20 + ["B"] * 80,
    })

    # numeric or categorical columns ko explicitly specify kr rhe hai,
    # taki report ko pata ho ki kis feature pr konsa test chalana hai.
    report = generate_drift_report(
        reference_df,
        current_df,
        ["age"],
        ["job"],
    )

    # age ki distribution change hui hai,
    # isliye numeric drift detect hona chahiye.
    assert report["numeric"]["age"]["drift_detected"] is True

    # job ki category distribution bhi change hui hai,
    # isliye categorical drift detect hoona chahiye.
    assert report["categorical"]["job"]["drift_detected"] is True

    # unified report me total monitored features ka count 
    # numeric + categorical features ka total hona chahiye.
    assert report["summary"]["total_features"] == 2

    # age or job dono me drift detect hau hai, isliye drifted featurs ki count 2 honi chahiye.
    assert report["summary"]["drifted_features"] == 2

    # kam se kam ek features drifted hone pr overall drifted status True hona chahiye.
    assert report["summary"]["overall_drift"] is True

    # reference or current datasets dono me 100 rowshai,
    # isliye report me dono sample sizes 100 hone chahiye.
    assert report["metadata"]["reference_samples"] == 100
    assert report["metadata"]["current_samples"] == 100

    # report me numeric significance threshold ka configured value
    # correctly store hona chahiye.
    assert report["configuration"]["numeric_significance_level"] == 0.05

    # Numeric drift ke liye configured effect threshold
    # correctly store hona chahiye.
    assert report["configuration"]["numeric_effect_threshold"] == 0.05

    # categorical drift ke liye configured significance threshold 
    # correctly store hona chahiye.
    assert report["configuration"]["categorical_significance_level"] == 0.05

# ye test check krta hai ki joab reference or current data same ho,
# to unified report correctly "no drift" report kre.
def test_generate_drift_report_no_drift():
    # reference data me baseline values define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "job": ["A"] * 50 + ["B"] * 50
    })

    # current data reference ke same hai
    # isliye kisi feature me distribution change nhi hui.
    current_df = reference_df.copy()

    # unified drift report generate kr rhe hai.
    report = generate_drift_report(
        reference_df,
        current_df,
        ["age"],
        ["job"],
    )

    # total monitored features 2 hona chahiye: 1 numeric + 1 categorical.
    assert report["summary"]["total_features"] == 2

    # koi feature drifted nhi hona chahiye.
    assert report["summary"]["drifted_features"] == 0

    # jab koi feature drifted nhi hai, overall drift bhi False hona chahiye.
    assert report["summary"]["overall_drift"] is False

    # individual numeric feature bhi non-drifted hona chahiye.
    assert report["numeric"]["age"]["drift_detected"] is False

    # individual categorical feature bhi no-drifted hoan chahiye.
    assert report["categorical"]["job"]["drift_detected"] is False


# ye test verify krta hai ki numeric effect threshold
# actually drift decision ko control kr rha hai.
def test_numeric_threshold_changes_drift_decision():
    # reference data ki age distribution define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
    })

    # current data me age distribution intentionally change hai.
    # isse KS statistic 0 or 1 ke bich rhega.
    current_df = pd.DataFrame({
        "age": [20] * 50 + [22] * 50,
    })

    # low effect threshold ke saath drift detect hona chahiye.
    report = generate_drift_report(
        reference_df,
        current_df,
        ["age"],
        [],
        numeric_effect_threshold=0.05,
    )

    # KS statistic 0.05 se greater hai,
    # isliye drift detect hona chahiye.
    assert report["numeric"]["age"]["drift_detected"] is True

    # Ab effect threshold ko 0.99 kr rhe hai.
    # isliye threshold actual KS statistic se bohut high hai.
    strict_report = generate_drift_report(
        reference_df,
        current_df,
        ["age"],
        [],
        numeric_effect_threshold=0.99,
    )

    # same data hone ke bawajood strict threshold ke kaaran
    # drift decision False hona chahiye.
    assert strict_report["numeric"]["age"]["drift_detected"] is False


# ye test verify krta hai ki categorical significance threshold
# actual drift decision lo control kr rha hai.
def test_categorical_threshold_changes_drift_decision():
    # reference data me A or B categories ka distribution almost balanced rkhta hai.
    reference_df = pd.DataFrame({
        "job": ["A"] * 50 + ["B"] * 50,
    })

    # current data me category distribution intentionally change kr rhe hai
    current_df = pd.DataFrame({
        "job": ["A"] * 20 + ["B"] * 80,
    })

    # normal significance level 0.05 le sath drift detect hona chahiye
    report = generate_drift_report(
        reference_df,
        current_df,
        [],
        ["job"],
        categorical_significance_level=0.05,
    )

    # p-value 0.05 se smaller hone pr categorical drift detect hoga
    assert report["categorical"]["job"]["drift_detected"] is True

    # ab significance level ko bahut small kr rhe hai.
    # isse drift detect krne ki condition much stricter ho jayegi.
    strict_report = generate_drift_report(
        reference_df,
        current_df,
        [],
        ["job"],
        categorical_significance_level=1e-100,
    )

    # same data hone ke bawajood strict significance threshold ke 
    # kaaran drift decision False hona chahiye.
    assert strict_report["categorical"]["job"]["drift_detected"] is False

# ye test verify krta hai ki jab koi feature drift nhi krta,
# system no_action recommendation deta hai.
def test_determine_drift_action_no_drift():
    # koi feature drift nhi hua hai.
    action = determine_drift_action(
        drifted_features=0,
        total_features=10,
    )

    # expected action no_action hona chahiye
    assert action == "no_action"

# ye test verify krta hai ki limited drift ke case me 
# system investigate recommend karta hai.
def test_determine_drift_action_investigate():
    # 2 out of 10 features drifted hai.
    # drift ratio = 20%, jo 50% threshold se kam hai,
    action = determine_drift_action(
        drifted_features=2,
        total_features=10,
    )

    # limited drift ke case me investigate krni chahiye.
    assert action == "investigate"

# ye test verify krta hai ki widespread drift ke case me 
# system retraining evaluation recommend krta hai.
def test_determine_drift_action_retraining_review():
    # 5 out of 10 features drifted hai.
    # drift ratio = 50%.
    action = determine_drift_action(
        drifted_features=5,
        total_features=10,
    )

    # 50% threshold cross hone pr retraining evaluate krenge.
    assert action == "evaluate_retraining"

# ye test verify krta hai ki unified drift report 
# action recommendation ko summary ke andar include kr rhe hai.
def test_generate_drift_report_includes_action():
    # reference data me 4 monitored features define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "balance": [100] * 50 + [101] * 50,
        "day": [1] * 50 + [2] * 50,
        "campaign": [1] * 50 + [2] * 50,
    })

    # sirf age distribution intentionally change hai.
    # baki features same hai
    current_df = reference_df.copy()
    current_df["age"] = [40] * 50 + [41] * 50

    # unified drift report generate kr rhe hai
    report = generate_drift_report(
        reference_df,
        current_df, 
        ["age", "balance", "day", "campaign"],
        [],
    )

    # 4 me se ek 1 feature drifted hai.
    # drift ratio = 25%, jo 50% retraining-review threshold se kam hai.
    assert report["summary"]["drifted_features"] == 1

    # isliye drifted action investigate hona chahiye.
    assert report["summary"]["action"] == "investigate"

# ye test verify krta hai ki widespread drift hone pr
# unified report evaluate_retraining action return krta hai.
def test_generate_drift_report_recommends_retraining_evaluation():
    # reference dataset me 4 monitored numeric features define kr rhe hai.
    reference_df = pd.DataFrame({
        "age": [20] * 50 + [21] * 50,
        "balance": [100] * 50 + [101] * 50,
        "day": [1] * 50 + [2] * 50,
        "campaign": [1] * 50 + [2] * 50,
    })

    # current dataset reference dataset ki copy hai.
    current_df = reference_df.copy()

    # sbhi 4 features me intentional distribution changes
    current_df["age"] = [40] * 50 + [41] * 50
    current_df["balance"] = [500] * 50 + [501] * 50
    current_df["day"] = [10] * 50 + [11] * 50
    current_df["campaign"] = [5] * 50 + [6] * 50

    # unified drift report generate kr rhe hai.
    report = generate_drift_report(
        reference_df,
        current_df,
        ["age", "balance", "day", "campaign"],
        [],
    )

    # sabhi 4 monitored features drifted hone chahiye.
    assert report["summary"]["drifted_features"] == 4

    # 4/4 = 100% drift ratio hai.
    # isliye retraining ko evaluate krne a action recommend hona chahiye.
    assert report["summary"]["action"] == "evaluate_retraining"