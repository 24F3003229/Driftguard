import pandas as pd

def load_data(path):
    return pd.read_csv(path, sep=";")

def inspect_data(df):
    print("Shape:", df.shape)

    print("\nFeatures:")
    print(df.drop(columns=["y"]).columns.tolist())

    print("\nTarget:")
    print(df["y"].value_counts())

    print("\nNumeric columns:")
    print(df.select_dtypes(include="number").columns.tolist())

    print("\nCategorical columns:")
    print(df.select_dtypes(exclude="number").columns.tolist())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\npdays value counts:")
    print(df["pdays"].value_counts().head(15))

    categorical_columns = df.select_dtypes(exclude="number").columns

    print("\nUnique values in categorical columns:")

    for column in categorical_columns:
        print(f"\n{column}:")
        print(df[column].value_counts().head(10))

if __name__ == "__main__":
    df = load_data("data/bank-full.csv")
    inspect_data(df)