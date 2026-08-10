import pandas as pd
from pathlib import Path


def load_data():

    file_path = (
        Path(__file__)
        .resolve()
        .parent
        .parent
        / "data"
        / "raw"
        / "sensor_measurements.csv"
    )

    return pd.read_csv(file_path)



def validate_missing_values(df):

    missing = df.isnull().sum()

    if missing.any():
        print("❌ Missing values detected:")
        print(missing[missing > 0])
        return False

    print("✅ No missing values")
    return True



def validate_amplitude(df):

    invalid = df[
        (df["amplitude"] < 0) |
        (df["amplitude"] > 1)
    ]

    if len(invalid) > 0:
        print(
            f"❌ Invalid amplitude values: {len(invalid)}"
        )
        return False

    print("✅ Amplitude values valid")
    return True



def validate_coordinates(df):

    invalid = df[
        (df["x"] < 0)
    ]

    if len(invalid) > 0:
        print(
            f"❌ Invalid coordinates: {len(invalid)}"
        )
        return False

    print("✅ Coordinates valid")
    return True



def run_validation():

    df = load_data()

    print(
        f"Loaded {len(df)} records"
    )

    checks = [
        validate_missing_values(df),
        validate_amplitude(df),
        validate_coordinates(df)
    ]

    if all(checks):
        print(
            "\n🎉 DATA VALIDATION PASSED"
        )
    else:
        print(
            "\n⚠️ DATA VALIDATION FAILED"
        )


if __name__ == "__main__":
    run_validation()