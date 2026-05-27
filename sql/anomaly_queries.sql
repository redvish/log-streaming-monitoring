USE log_monitoring;

-- 1. Минуты с большим количеством запросов
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
HAVING COUNT(*) >= 30
ORDER BY requests_count DESC;

-- 2. Минуты с большим количеством ошибок 4xx/5xx
SELECT
    from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:mm:00'
    ) AS minute_window,
    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS errors_count
FROM processed_logs
GROUP BY from_unixtime(
        unix_timestamp(CAST(event_time AS STRING), 'yyyy-MM-dd HH:mm:ss'),
        'yyyy-MM-dd HH:mm:00'
    )
HAVING SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) >= 10
ORDER BY errors_count DESC;

-- 3. IP-адреса с большим количеством ошибок 4xx/5xx
SELECT
    ip,
    COUNT(*) AS errors_count
FROM processed_logs
WHERE status_code >= 400
GROUP BY ip
HAVING COUNT(*) >= 10
ORDER BY errors_count DESC;

-- 4. URL с большим количеством серверных ошибок 5xx
SELECT
    url,
    COUNT(*) AS server_errors_5xx
FROM processed_logs
WHERE status_code >= 500 AND status_code < 600
GROUP BY url
HAVING COUNT(*) >= 5
ORDER BY server_errors_5xx DESC;
