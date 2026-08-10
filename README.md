# AcousticSense Pipeline
**Python | PySpark | AWS S3 | AWS Glue Jobs | AWS Glue Data Catalog | Amazon Athena | Parquet | Plotly**

End-to-End AWS Data Engineering Pipeline for Industrial Acoustic Sensor Analytics.

---

# 🔷 Project Overview

AcousticSense Pipeline is an end-to-end data engineering project that simulates the processing of industrial acoustic sensor data.

The project demonstrates a complete cloud-based workflow for collecting, validating, transforming, storing, and analyzing sensor measurements using modern data engineering technologies.

The pipeline generates synthetic ultrasonic sensor data and stores raw measurements in an Amazon S3 data lake.

AWS Glue Jobs using PySpark perform data quality validation and scalable ETL processing, transforming raw CSV data into optimized Parquet datasets stored in the processed layer.

Processed data is catalogued using AWS Glue Data Catalog and analyzed using Amazon Athena. Statistical anomaly detection is applied to identify measurements that significantly differ from typical sensor behaviour, and results are visualized through an interactive 3D acoustic signal visualization.

The project is inspired by industrial inspection systems where large-scale sensor data is processed to identify potential structural anomalies and generate actionable insights.

---

# 🎯 Business Problem

Industrial inspection systems generate large volumes of sensor data that must be processed reliably before any analysis or machine learning can be performed.

Raw sensor measurements may contain:
- missing values,
- invalid measurements,
- inconsistent formats,
- abnormal signal readings.

The goal of this project is to build a reliable data pipeline that ensures:

- data quality before downstream processing,
- efficient storage of processed datasets,
- scalable cloud-based data management,
- preparation of sensor data for anomaly detection and visualization.

---

# 🏗️ Data Pipeline Architecture

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

# 🔄 Pipeline Workflow

## 1. Data Generation

Synthetic acoustic sensor measurements are generated using Python.

Generated attributes include:

- sensor_id
- timestamp
- x, y, z coordinates
- frequency
- temperature
- signal amplitude


## 2. Data Validation

AWS Glue Job performs automated data quality checks to ensure data reliability.

Validation checks include:

- missing value detection
- amplitude range validation
- coordinate validation
- schema consistency checks


## 3. ETL Processing with AWS Glue Job

Raw CSV files stored in Amazon S3 are processed using an AWS Glue Job built with PySpark.

The Glue Job performs:

- data quality checks,
- schema and data type conversion,
- timestamp formatting,
- chronological sorting,
- feature engineering,
- temperature rounding,
- conversion from CSV to optimized Parquet format.

The transformed dataset is stored in the processed layer of the S3 data lake.
AWS Glue job execution logs are monitored through Amazon CloudWatch, providing visibility into ETL runs, data quality checks, and job completion status.

<img width="820" height="288" alt="logs" src="https://github.com/user-attachments/assets/54f3556d-1233-460a-b9f6-6b1438854f3f" />

---

# 🗂️ AWS Glue Data Catalog

AWS Glue Crawler was used to automatically discover the schema of processed Parquet files stored in Amazon S3.

The crawler created a metadata table in AWS Glue Data Catalog, enabling serverless SQL analytics through Amazon Athena.

Created catalog schema:

<img width="1562" height="478" alt="1" src="https://github.com/user-attachments/assets/03715c75-897b-4fc8-b9ab-6ee377c95b10" />

---

# 📊 Athena Analytics

Amazon Athena was used to perform SQL-based analysis directly on the processed Parquet data stored in Amazon S3.

The query ranks potentially abnormal acoustic measurements by calculating a sensor-specific statistical baseline.

A higher z-score indicates that the measurement significantly deviates from the sensor's typical behaviour, helping identify potential areas requiring further investigation.

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

## 🌐 3D Acoustic Anomaly Visualization

The visualization was created using Python and Plotly.

Each point represents a spatial sensor measurement:

- X/Y/Z coordinates represent physical location
- Point size represents acoustic amplitude
- Color represents anomaly classification based on statistical deviation

Potential anomalies are highlighted for further inspection.

<img width="902" height="565" alt="3" src="https://github.com/user-attachments/assets/3dc61c46-02ef-462a-8331-864616487f82" />

---

# 🧪 Technologies Used

## Programming

- Python
- Pandas
- NumPy
- Plotly


## Data Engineering

- ETL pipeline design
- Data quality validation
- Data transformation
- Apache Parquet

## Data Processing

- PySpark
- AWS Glue Jobs

## AWS Cloud

- Amazon S3
- AWS Glue Jobs
- AWS Glue Crawler
- AWS Glue Data Catalog
- Amazon Athena
- Amazon CloudWatch
- AWS CLI
- boto3

---

# 📁 Project Structure

```
acoustic-sense-pipeline/

├── src/
│   ├── generate_data.py
│   ├── upload_to_s3.py
│   └── visualize_3d.py
├── glue_jobs/
│   └── transform_sensor_data.py
├── requirements.txt
└── README.md
```

---

# 🚀 How to Run the Project

```
1. Generate sensor data

python src/generate_data.py


2. Upload raw data to Amazon S3

python src/upload_to_s3.py


3. Run AWS Glue Job

AWS Glue Job performs data quality checks and transforms raw CSV data into Parquet format.


4. Run Glue Crawler

Update metadata catalog.


5. Query processed data using Amazon Athena.
```

---

# 🔮 Future Improvements

Potential future extensions:

- Automated pipeline orchestration using AWS Step Functions or Apache Airflow
- Real-time sensor ingestion using streaming services
- Machine learning-based anomaly detection models
- Integration with client reporting dashboards
- Processing of real ultrasonic waveform data
