import pandas as pd

# Load original earthquake data
df = pd.read_csv("global_earthquakes_seismic.csv")
print("Original shape:", df.shape)
print("Missing values:", df.isna().sum().sum())
print("Duplicate IDs:", df["id"].duplicated().sum())

# Clean blanks, duplicates, and non-earthquake events
df = df.replace(r"^\s*$", pd.NA, regex=True)
df = df.drop_duplicates().drop_duplicates(subset="id")
df = df.loc[df["type"].eq("earthquake")].copy()

# Correct data types and remove invalid critical records
df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True, errors="coerce")
for col in ["latitude", "longitude", "depth", "mag"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["id", "time", "latitude", "longitude", "depth", "mag"])
df = df.loc[df.latitude.between(-90, 90) & df.longitude.between(-180, 180) & (df.depth >= 0) & (df.mag >= 0)].copy()

# Add useful date fields, remove redundant narrative fields, sort and save
df["year"] = df.time.dt.year
df["month"] = df.time.dt.strftime("%Y-%m")
df["date"] = df.time.dt.strftime("%Y-%m-%d")
df = df.drop(columns=["evidence_span", "cot_rationale", "title"], errors="ignore")
df = df.sort_values("time").reset_index(drop=True)
df.to_csv("global_earthquakes_cleaned.csv", index=False)
print("Cleaned shape:", df.shape)
