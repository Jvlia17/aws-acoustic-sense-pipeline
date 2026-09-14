# AcousticSense Pipeline
**Python | PySpark | AWS Lambda | Amazon S3 | AWS Glue Jobs | AWS Glue Data Catalog | Amazon Athena | Parquet | Plotly**

End-to-End AWS Data Engineering Pipeline for Industrial Acoustic Sensor Analytics.

---

# Project Overview

AcousticSense Pipeline is an event-driven AWS data engineering project for processing synthetic industrial acoustic sensor data.

Python generates sensor measurements that are uploaded to Amazon S3. New files trigger AWS Lambda, which starts an AWS Glue PySpark job with the uploaded file path. Glue validates and transforms the data, then stores optimized Parquet datasets in S3.

Processed data is catalogued with AWS Glue Data Catalog and analyzed using Amazon Athena for statistical anomaly detection. Results are visualized as an interactive 3D representation of sensor measurements.

---

# Business Problem

Industrial sensor data requires reliable validation and transformation before analysis. This project builds an automated pipeline that ensures data quality, efficient storage, and prepares sensor measurements for anomaly detection.

---

# Data Pipeline Architecture

The pipeline follows a cloud-based ETL architecture:

```text
Synthetic Sensor Data
        |
        v
Python Data Generation
        |
        v
Raw CSV Dataset
        |
        v
Amazon S3 (raw/)
        |
        | ObjectCreated Event
        v
AWS Lambda
        |
        | Start Glue Job
        v
AWS Glue Job (PySpark)
        |
        |
        ├── Data Validation
        ├── Data Transformation
        ├── Feature Engineering
        └── Parquet Conversion
        |
        v
Amazon S3 (processed/)
        |
        v
AWS Glue Crawler
        |
        v
AWS Glue Data Catalog
        |
        v
Amazon Athena Analytics
        |
        v
Anomaly Detection
        |
        v
3D Visualization
```

---

# Pipeline Workflow

## 1. Data Generation

Python generates synthetic acoustic sensor measurements containing spatial, temporal, signal, and environmental attributes.

The generated CSV dataset is uploaded to the raw/ prefix of the Amazon S3 bucket.


## 2. Event-Driven Trigger

When a new CSV object is uploaded to the S3 `raw/` prefix, an `ObjectCreated` event triggers AWS Lambda. The function starts the Glue PySpark job and dynamically passes the uploaded file path through the `INPUT_PATH` parameter.

## 3. ETL Processing with AWS Glue Job

The AWS Glue Job uses PySpark to validate and transform the input data, perform feature engineering, and convert CSV files into optimized Parquet datasets.

Data quality checks cover missing values, invalid amplitudes, and invalid coordinates. If validation fails, the pipeline stops before invalid data reaches the processed layer.

The transformed dataset is stored as optimized Parquet files in the S3 `processed/` layer.

AWS Glue Job execution logs are monitored through Amazon CloudWatch, providing visibility into ETL runs, data quality checks, and job completion status.

<img width="820" height="288" alt="logs" src="https://github.com/user-attachments/assets/54f3556d-1233-460a-b9f6-6b1438854f3f" />

---

# AWS Glue Data Catalog

AWS Glue Crawler was used to automatically discover the schema of processed Parquet files stored in Amazon S3.

The crawler created a metadata table in AWS Glue Data Catalog, enabling serverless SQL analytics through Amazon Athena.

Created catalog schema:

<img width="1562" height="478" alt="1" src="https://github.com/user-attachments/assets/03715c75-897b-4fc8-b9ab-6ee377c95b10" />

---

# Athena Analytics

Amazon Athena is used to analyze the processed Parquet data stored in Amazon S3. 

Sensor-specific z-scores are calculated to identify measurements that significantly deviate from typical signal behaviour.


```sql
WITH sensor_statistics AS (
    SELECT
        sensor_id,
        AVG(amplitude) AS avg_amplitude,
        STDDEV(amplitude) AS std_amplitude
    FROM processed
    GROUP BY sensor_id
)

SELECT
    p.sensor_id,
    p.timestamp,
    p.amplitude,
    ROUND(
        (p.amplitude - s.avg_amplitude) / s.std_amplitude,
        2
    ) AS z_score
FROM processed p
JOIN sensor_statistics s
    ON p.sensor_id = s.sensor_id
ORDER BY z_score DESC
LIMIT 10;
```

The query returned the measurements with the highest deviation from each sensor's normal signal pattern:

<img width="1453" height="705" alt="2" src="https://github.com/user-attachments/assets/3c30a3e1-dbc1-44ea-a1d4-21350382f785" />

These results can be used as input for further anomaly investigation, reporting pipelines, or visualization of potential defect locations.

---

## 3D Acoustic Anomaly Visualization

An interactive 3D Plotly visualization shows sensor measurements by spatial location, amplitude, and anomaly classification.

<img width="902" height="565" alt="3" src="https://github.com/user-attachments/assets/3dc61c46-02ef-462a-8331-864616487f82" />

---

# Technologies Used

## Programming

- Python
- Pandas
- NumPy
- Plotly
- boto3

## Data Engineering

- ETL pipeline design
- Event-driven architecture
- Data quality validation
- Data transformation

## Data Processing

- PySpark
- - Apache Parquet

## AWS Cloud

- Amazon S3
- S3 Event Notifications
- AWS Lambda
- AWS Glue Jobs
- AWS Glue Crawler
- AWS Glue Data Catalog
- Amazon Athena
- Amazon CloudWatch
- AWS CLI

---

# Project Structure

```
acoustic-sense-pipeline/

├── src/
│   ├── generate_data.py
│   ├── upload_to_s3.py
│   └── visualize_3d.py
│
├── glue_jobs/
│   └── transform_sensor_data.py
│
├── lambda/
│   └── s3_trigger.py
│
├── requirements.txt
└── README.md
```

---

# How to Run the Project

```
1. Generate sensor data
python src/generate_data.py

2. Upload raw data to Amazon S3
python src/upload_to_s3.py
The generated CSV file is uploaded to the S3 raw/ prefix.

3. Event-driven ETL processing
The S3 upload automatically triggers the Lambda function.
Lambda starts the AWS Glue Job and passes the uploaded object's S3 path as the INPUT_PATH parameter.
The Glue Job validates and transforms the data and writes the resulting Parquet dataset to the processed/ prefix.

4. Run Glue Crawler
Update the AWS Glue Data Catalog metadata after new processed datasets are created.

5. Query processed data using Amazon Athena
Use Athena to perform SQL analysis and identify potential acoustic anomalies.
```

---

# Future Improvements

Potential future extensions:

- adding Amazon SQS between S3 and Lambda for event buffering and decoupling,
- orchestration using AWS Step Functions or Apache Airflow for more complex workflows,
- real-time sensor ingestion using streaming services,
- machine learning-based anomaly detection models,
- integration with client reporting dashboards,
- processing of real ultrasonic waveform data.
