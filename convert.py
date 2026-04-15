import sqlite3

import pandas as pd


def normalize_coordinates(row):
    first = float(row["raw_latitude"])
    second = float(row["raw_longitude"])

    if first > 40 and second < 40:                               
        return pd.Series({"latitude": second, "longitude": first})
        return pd.Series({"latitude": first, "longitude": second})


df = pd.read_excel("latlong.xlsx", engine="openpyxl")
df = df.rename(
    columns={
        "Service no.": "service_no",
        "lat": "raw_latitude",
        "long": "raw_longitude",
    }
)

df["service_no"] = (
    df["service_no"]
    .astype(str)
    .str.replace(r"\.0$", "", regex=True)
    .str.strip()
)
df[["latitude", "longitude"]] = df.apply(normalize_coordinates, axis=1)
df = df[["service_no", "latitude", "longitude"]].dropna()

conn = sqlite3.connect("services.db")
df.to_sql("services", conn, if_exists="replace", index=False)
conn.close()

print(f"Database ready with {len(df)} services.")
