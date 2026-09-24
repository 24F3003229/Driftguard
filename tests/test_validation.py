import pandas as pd

from src.data.validation import validate_columns

def test_valid_columns():
    df = pd.DataFrame(
        columns=[
            "age",
            "job",
            "marital",
            "education",
            "default",
            "balance",
            "housing",
            "loan",
            "contact",
            "day",
            "month",
            "duration",
            "campaign",
            "pdays",
            "previous",
            "poutcome",
            "y",
        ]
    )

    missing, unexpected = validate_columns(df)

    assert missing == []
    assert unexpected == []

def test_missing_columns():
    df = pd.DataFrame(
        columns=[
            "age",
            "job",
            "marital",
        ]
    )

    missing, unexpected = validate_columns(df)

    assert "education" in missing
    assert "balance" in missing

def test_unexpected_column():
    df = pd.DataFrame(
        columns=[
            "age",
            "job",
            "marital",
            "education",
            "default",
            "balance",
            "housing",
            "loan",
            "contact",
            "day",
            "month",
            "duration",
            "campaign",
            "pdays",
            "previous",
            "poutcome",
            "y",
            "unexpected",
        ]
    )

    missing, unexpected = validate_columns(df)

    assert missing == []
    assert "unexpected" in unexpected