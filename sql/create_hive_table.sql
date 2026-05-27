CREATE DATABASE IF NOT EXISTS log_monitoring;

DROP TABLE IF EXISTS log_monitoring.processed_logs;

CREATE EXTERNAL TABLE log_monitoring.processed_logs (
    json_str STRING,
    ip STRING,
    `timestamp` STRING,
    method STRING,
    url STRING,
    status_code INT,
    response_size INT,
    user_agent STRING,
    event_time TIMESTAMP
)
STORED AS PARQUET
LOCATION '/user/student/log_monitoring/processed_logs';
