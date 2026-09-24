import pandas as pd 

EXPECTED_COLUMNS = [
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

NUMERIC_COLUMNS = [
    "age",
    "balance",
    "day",
    "duration",
    "campaign",
    "pdays",
    "previous",
]

CATEGORICAL_COLUMNS = [
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

def validate_columns(df):
    actual_columns = list(df.columns)

    missing_columns = [
        column 
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    unexpected_columns = [
        column 
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    return missing_columns, unexpected_columns

if __name__ == "__main__":
    df = pd.read_csv("data/bank-full.csv", sep=";")

    missing, unexpected = validate_columns(df)

    print("Missing columns:", missing)
    print("Unexpected columns:", unexpected)