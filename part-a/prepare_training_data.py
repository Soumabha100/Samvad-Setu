import pandas as pd
from preprocess import preprocess_complaint

INPUT_FILE = "dataset/complaints.csv"
OUTPUT_FILE = "dataset/processed_complaints.csv"

df = pd.read_csv(INPUT_FILE)

df["text"] = df["text"].apply(preprocess_complaint)

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("========== DATA PREPARATION ==========")
print("Original rows :", len(pd.read_csv(INPUT_FILE)))
print("Processed rows:", len(df))
print("Columns       :", list(df.columns))
print("Output file   :", OUTPUT_FILE)
print("=======================================")