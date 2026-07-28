import boto3
from pathlib import Path


BUCKET_NAME = "acoustic-sense-pipeline"


BASE_DIR = Path(__file__).resolve().parent.parent


s3 = boto3.client("s3")


def upload_file(local_file, s3_key):

    s3.upload_file(
        str(local_file),
        BUCKET_NAME,
        s3_key
    )

    print(
        f"Uploaded {local_file} -> s3://{BUCKET_NAME}/{s3_key}"
    )


if __name__ == "__main__":

    raw_file = (
        BASE_DIR
        / "data"
        / "raw"
        / "sensor_measurements.csv"
    )

    processed_file = (
        BASE_DIR
        / "data"
        / "processed"
        / "sensor_measurements.parquet"
    )


    upload_file(
        raw_file,
        "raw/sensor_measurements.csv"
    )


    upload_file(
        processed_file,
        "processed/sensor_measurements.parquet"
    )