# AcousticSense Pipeline
**Python | AWS S3 | AWS Glue | Amazon Athena | Parquet | Plotly**

End-to-End AWS Data Engineering Pipeline for Industrial Acoustic Sensor Analytics.

---

# 🔷 Project Overview

AcousticSense Pipeline is an end-to-end data engineering project that simulates the processing of industrial acoustic sensor data.

The project demonstrates a complete cloud-based workflow for collecting, validating, transforming, storing, and analyzing sensor measurements using modern data engineering technologies.

The pipeline generates synthetic ultrasonic sensor data, performs automated data quality validation, transforms raw datasets into optimized Parquet format, and stores processed data in an Amazon S3 data lake.

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
Data Validation
        |
        v
Data Transformation
        |
        v
Parquet Dataset
        |
        v
Amazon S3 Data Lake
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

Automated validation checks ensure data reliability:

- missing value detection
- amplitude range validation
- coordinate validation
- schema consistency checks


## 3. Data Transformation

Raw CSV files are transformed into optimized Parquet format.

Transformations include:

- timestamp formatting
- sorting measurements chronologically
- feature generation
- data type optimization


## 4. Cloud Storage and Data Catalog

Processed datasets are stored in Amazon S3 using a data lake structure.

AWS Glue Crawler automatically discovers the schema and creates metadata tables in AWS Glue Data Catalog.

S3 structure:

```
acoustic-sense-pipeline/

├── raw/

│   └── sensor_measurements.csv

├── processed/

│   └── sensor_measurements.parquet

└── athena-results/

    └── query-results.csv
```
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
- Data validation
- Data transformation
- Apache Parquet


## AWS Cloud

- Amazon S3
- AWS Glue Crawler
- AWS Glue Data Catalog
- Amazon Athena
- AWS CLI
- boto3


## Data Processing

- PyArrow

---

# 📁 Project Structure

```
acoustic-sense-pipeline/

├── data/

│   ├── raw/

│   └── processed/


├── src/

│   ├── generate_data.py

│   ├── validation.py

│   ├── preprocessing.py

│   ├── upload_to_s3.py

│   └── visualize_3d.py


├── reports/

│   └── acoustic_anomaly_visualization.html


├── requirements.txt

└── README.md
```

---

# 🚀 How to Run the Project

1. Install dependencies
```
pip install -r requirements.txt
```

2. Generate sensor data
```
python src/generate_data.py
```

3. Validate data quality
```
python src/validation.py
```

4. Transform data
```
python src/preprocessing.py
```

5. Upload data to AWS S3
```
python src/upload_to_s3.py
```

---

# 🔮 Future Improvements

Potential future extensions:

- Automated pipeline orchestration using AWS Step Functions or Apache Airflow
- Real-time sensor ingestion using streaming services
- Machine learning-based anomaly detection models
- Integration with client reporting dashboards
- Processing of real ultrasonic waveform data
