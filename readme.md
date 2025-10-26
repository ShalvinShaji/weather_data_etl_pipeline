# Weather ETL Pipeline

![Weather ETL Diagram](diagrams/weather_etl.png)

## Project Overview
This project is a **serverless ETL pipeline** that ingests, processes, and stores weather data for analytics. The architecture is layered and uses AWS managed services for scalability and reliability.

---

## Architecture Layers

### 1. Ingest Layer
- **Weather API**: Fetches real-time weather data every 5 minutes.
- **AWS Lambda**: Performs ETL processing on incoming data.
- **Kinesis Firehose**: Streams data into Raw S3.

### 2. Raw Zone
- **Raw S3 Bucket**: Stores unprocessed JSON data (`YY/MM/DD/HH`).

### 3. Silver Zone
- **Glue Streaming Jobs**: Cleans and enriches data continuously.
- **Silver S3 Bucket**: Stores processed data for downstream transformations.

### 4. Gold Zone
- **Glue Batch Jobs**: Aggregates daily data.
- **Gold S3 Bucket**: Stores curated datasets for analytics.

### 5. Analytics
- **Amazon Redshift**: Hosts datasets for dashboards and BI reporting.

---

## Technology Stack

- **AWS Services**: Lambda, Kinesis Firehose, S3, Glue (Streaming & Batch), Redshift
- **Python**: ETL scripts
- **JSON**: Data format from Weather API


