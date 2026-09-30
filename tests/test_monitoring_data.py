import pandas as pd
from src.data.monitoring_data import (
    prepare_monitoring_datasets,
)

# ye test verify krta hai ki monitoring ke liye
# reference or current datasets correctly prepare ho rhe hai.
def test_prepare_monitoring_datasets(tmp_path):
    # small synthetic dataset create kr rhe hai.
    df = pd.DataFrame({
        "age": list(range(20, 40)),
        "balance": list(range(100, 120)),
        "y": ["no", "yes"] * 10,
    })

    # temporary CSV file create kr rhe hai.
    data_path = tmp_path / "bank-full.csv"

    # test dataset ko same format me save kr rhe hai.
    # jaisa original Bank Marketing dataset use krta hai.
    df.to_csv(
        data_path,
        sep=";",
        index=False,
    )

    # monitoring datasets prepare kr rhe hai.
    reference_df, reference_evaluation_df, current_df, y_test = (
        prepare_monitoring_datasets(
            data_path=data_path,
            current_age_shift=5,
        )
    )

    # reference dataset me target column nhi hona chahiye.
    assert "y" not in reference_df.columns

    # reference evaluation dataset bhi taget column caontain nhi krna chahiye.
    assert "y" not in reference_evaluation_df.columns

    # current dataset me bhi target columns nhi hona chahiye.
    assert "y" not in current_df.columns

    # reference or current evaluation datasets ka same shape hona chahiye.
    assert reference_evaluation_df.shape == current_df.shape

    # reference or current datasets ke columns same hone chahiye.
    assert list(reference_df.columns)  == list(current_df.columns)

    # donno datasets ke same features hone chahiye.
    assert list(reference_evaluation_df.columns) == list(current_df.columns)

    # test labels return hone chahiye.
    assert len(y_test) == len(current_df)

    # current age values reference/test source ke comparision me
    # 5 units shift honi chahiye.
    assert current_df["age"].min() >= 30

    # current dataset me simulated age shift apply hua hona chahiye.
    assert (
        current_df["age"] == reference_evaluation_df["age"] + 5
    ).all()