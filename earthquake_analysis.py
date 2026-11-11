from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("global_earthquakes_cleaned.csv")
df["time"] = pd.to_datetime(df["time"], utc=True, format="mixed")
out = Path("visualizations")
out.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")

# Sorting: find the largest events
print(df.sort_values("mag", ascending=False)[["place", "mag", "depth"]].head(10))
# Filtering: focus on stronger events
strong = df.loc[df["mag"] >= 6]
print("Magnitude 6+ events:", len(strong), "Percentage:", round(len(strong) / len(df) * 100, 2))
# Grouping: compare tectonic regions
region = "tectonic_boundary_zone"
print(df.groupby(region).agg(count=("id", "count"), mean_magnitude=("mag", "mean"), mean_depth=("depth", "mean")).round(2))
# Descriptive, correlation and distribution statistics
print(df[["mag", "depth"]].describe())
print("Magnitude mode:", df.mag.mode().iloc[0])
print("Magnitude skewness:", df.mag.skew())
print("Magnitude-depth correlation:", df.mag.corr(df.depth))

fig, ax = plt.subplots(figsize=(11, 6))
counts = df[region].value_counts()
sns.barplot(x=counts.values, y=counts.index, color="steelblue", ax=ax)
ax.set(title="Earthquakes by Tectonic Region", xlabel="Number of Earthquakes", ylabel="Tectonic Region")
fig.tight_layout(); fig.savefig(out / "earthquakes_by_region.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x="mag", bins=25, color="orange", edgecolor="black", ax=ax)
ax.set(title="Distribution of Earthquake Magnitudes", xlabel="Magnitude", ylabel="Number of Earthquakes")
fig.tight_layout(); fig.savefig(out / "magnitude_distribution.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x="depth", y="mag", alpha=0.25, color="purple", label="Earthquakes", s=18, ax=ax)
ax.set(title="Earthquake Magnitude vs Depth", xlabel="Depth (km)", ylabel="Magnitude")
ax.legend(); fig.tight_layout(); fig.savefig(out / "magnitude_vs_depth.png", dpi=160); plt.close(fig)

monthly = df.set_index("time").resample("MS").size()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly.index, monthly.values, marker="o", color="green", label="Monthly earthquakes")
ax.set(title="Recorded Earthquakes by Month", xlabel="Month", ylabel="Number of Earthquakes")
ax.tick_params(axis="x", rotation=45); ax.legend()
fig.tight_layout(); fig.savefig(out / "earthquakes_over_time.png", dpi=160); plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(df[["mag", "depth"]].corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
ax.set_title("Magnitude and Depth Correlation")
fig.tight_layout(); fig.savefig(out / "correlation_heatmap.png", dpi=160); plt.close(fig)
print("Saved five charts to", out)
