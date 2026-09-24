import pandas as pd

df = pd.read_csv("data/bank-full.csv", sep=";")

target_counts = df["y"].value_counts()

total = target_counts.sum()

print("Target counts:")
print(target_counts)

print("\nTarget percentages:")

for label, count in target_counts.items():
    percentage = count / total * 100
    print(f"{label}: {percentage:.2f}%")