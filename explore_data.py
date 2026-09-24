import pandas as pd

df = pd.read_csv("data/bank-full.csv", sep=";")

print("Dataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn data types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nTarget distribution:")
print(df["y"].value_counts())