USE log_monitoring;

-- 1. Количество запросов по минутам
SELECT
    from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:mm:00'
    ) AS minute_window,
    COUNT(*) AS requests_count
FROM processed_logs
GROUP BY from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:mm:00'
    )
ORDER BY minute_window;

-- 2. Количество 4xx и 5xx ошибок по минутам
SELECT
    from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:mm:00'
    ) AS minute_window,
    SUM(CASE WHEN status_code >= 400 AND status_code < 500 THEN 1 ELSE 0 END) AS client_errors_4xx,
    SUM(CASE WHEN status_code >= 500 AND status_code < 600 THEN 1 ELSE 0 END) AS server_errors_5xx
FROM processed_logs
GROUP BY from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:mm:00'
    )
ORDER BY minute_window;

-- 3. Количество запросов по часам
SELECT
    from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:00:00'
    ) AS hour_window,
    COUNT(*) AS requests_count
FROM processed_logs
GROUP BY from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:00:00'
    )
ORDER BY hour_window;
