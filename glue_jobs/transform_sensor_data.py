import sys

from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql import functions as F


# Initialize Glue context

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init("acoustic-sense-transform-job", {})


# S3 paths

INPUT_PATH = "s3://acoustic-sense-pipeline/raw/sensor_measurements.csv"

OUTPUT_PATH = "s3://acoustic-sense-pipeline/processed/"


# -----------------------------------
# 1. Read raw data
# -----------------------------------

df = (
    spark.read
    .option("header", "true")
    .csv(INPUT_PATH)
)

print(f"Loaded rows: {df.count()}")


# -----------------------------------
# 2. Data type conversion
# -----------------------------------

df = (
    df
    .withColumn(
        "timestamp",
        F.to_timestamp("timestamp")
    )
    .withColumn(
        "x",
        F.col("x").cast("double")
    )
    .withColumn(
        "y",
        F.col("y").cast("double")
    )
    .withColumn(
        "z",
        F.col("z").cast("double")
    )
    .withColumn(
        "frequency",
        F.col("frequency").cast("double")
    )
    .withColumn(
        "temperature",
        F.col("temperature").cast("double")
    )
    .withColumn(
        "amplitude",
        F.col("amplitude").cast("double")
    )
)


# -----------------------------------
# 3. Data quality checks
# -----------------------------------

# Missing values

missing_values = (
    df
    .filter(
        F.col("sensor_id").isNull()
        | F.col("timestamp").isNull()
        | F.col("amplitude").isNull()
        | F.col("frequency").isNull()
    )
    .count()
)

if missing_values > 0:
    raise Exception(
        f"Data quality check failed: {missing_values} rows contain missing values"
    )


# Invalid amplitude

invalid_amplitude = (
    df
    .filter(
        F.col("amplitude") < 0
    )
    .count()
)

if invalid_amplitude > 0:
    raise Exception(
        f"Data quality check failed: {invalid_amplitude} rows have invalid amplitude values"
    )


# Invalid coordinates

invalid_coordinates = (
    df
    .filter(
        F.col("x").isNull()
        | F.col("y").isNull()
        | F.col("z").isNull()
    )
    .count()
)

if invalid_coordinates > 0:
    raise Exception(
        f"Data quality check failed: {invalid_coordinates} rows have invalid coordinates"
    )


print("Data quality checks passed successfully")


# -----------------------------------
# 4. Transformations
# -----------------------------------

# Sort by timestamp

df = df.orderBy("timestamp")


# Feature engineering

df = df.withColumn(
    "signal_strength",
    F.col("amplitude") * F.col("frequency")
)


# Round temperature

df = df.withColumn(
    "temperature",
    F.round("temperature", 2)
)


# -----------------------------------
# 5. Write processed data
# -----------------------------------

(
    df.write
    .mode("overwrite")
    .parquet(OUTPUT_PATH)
)


print("ETL job completed successfully")


job.commit()