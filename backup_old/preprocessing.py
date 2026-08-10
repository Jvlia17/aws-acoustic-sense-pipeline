import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "sensor_measurements.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)


def load_raw_data():

    return pd.read_csv(
        RAW_FILE,
        parse_dates=["timestamp"]
    )


def transform_data(df):

    # sortowanie po czasie
    df = df.sort_values(
        "timestamp"
    )

    # dodajemy nową cechę
    # poziom sygnału

    df["signal_strength"] = (
        df["amplitude"]
        *
        df["frequency"]
    )

    # zaokrąglamy temperaturę

    df["temperature"] = (
        df["temperature"]
        .round(2)
    )

    return df



def save_processed_data(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_DIR
        /
        "sensor_measurements.parquet"
    )

    df.to_parquet(
        output_file,
        index=False
    )

    print(
        f"Saved: {output_file}"
    )



if __name__ == "__main__":

    df = load_raw_data()

    print(
        f"Loaded {len(df)} rows"
    )


    df = transform_data(df)


    save_processed_data(df)

    print(df.head())