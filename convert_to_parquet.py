import pandas as pd

print("Converting... this may take 5–15 minutes")

csv_path = "your_cleaned_dataset.csv"
parquet_path = "your_cleaned_dataset.parquet"

df = pd.read_csv(csv_path)
df.to_parquet(parquet_path, engine="pyarrow", index=False)

print("✅ Conversion completed successfully!")
