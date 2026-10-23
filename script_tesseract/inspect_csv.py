import pandas as pd

csv_path = r"D:\code material 2.0\akshar-setu-v2\data\lines\OCR-Bench1000-Gujarati\test.csv"

df = pd.read_csv(csv_path)

print("Columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)