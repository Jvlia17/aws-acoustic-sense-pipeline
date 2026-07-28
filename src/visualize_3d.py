import pandas as pd
import plotly.express as px


# ==============================
# 1. Load processed Parquet data
# ==============================

df = pd.read_parquet(
    "../data/processed/sensor_measurements.parquet"
)

print("Loaded data:")
print(df.head())
print("\nColumns:")
print(df.columns)
print("\nShape:")
print(df.shape)


# ==============================
# 2. Calculate sensor baseline
# ==============================

sensor_stats = (
    df.groupby("sensor_id")["amplitude"]
    .agg(
        avg_amplitude="mean",
        std_amplitude="std"
    )
    .reset_index()
)


# Add sensor statistics to every measurement
df = df.merge(
    sensor_stats,
    on="sensor_id",
    how="left"
)


# Calculate anomaly score
df["z_score"] = (
    (df["amplitude"] - df["avg_amplitude"])
    /
    df["std_amplitude"]
)


print("\nData with anomaly score:")
print(
    df[
        [
            "sensor_id",
            "amplitude",
            "avg_amplitude",
            "std_amplitude",
            "z_score"
        ]
    ].head()
)


# ==============================
# 3. Create anomaly category
# ==============================

df["status"] = df["z_score"].apply(
    lambda x: "Potential anomaly" if x > 3 else "Normal"
)


print("\nAnomaly counts:")
print(df["status"].value_counts())


# ==============================
# 4. 3D Visualization
# ==============================

fig = px.scatter_3d(
    df,
    x="x",
    y="y",
    z="z",
    color="status",
    size="amplitude",
    hover_data=[
        "sensor_id",
        "timestamp",
        "amplitude",
        "z_score"
    ],
    title="3D Acoustic Signal Anomaly Visualization"
)


fig.update_layout(
    scene=dict(
        xaxis_title="X Position",
        yaxis_title="Y Position",
        zaxis_title="Z Position"
    )
)


fig.show()