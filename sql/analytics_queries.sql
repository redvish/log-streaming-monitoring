USE log_monitoring;

-- 1. Общее количество запросов
SELECT COUNT(*) AS total_requests
FROM processed_logs;

-- 2. Распределение HTTP-кодов
SELECT 
    status_code,
    COUNT(*) AS requests_count
FROM processed_logs
GROUP BY status_code
ORDER BY status_code;

-- 3. Топ URL по количеству запросов
SELECT 
    url,
    COUNT(*) AS requests_count
FROM processed_logs
GROUP BY url
ORDER BY requests_count DESC
LIMIT 10;

-- 4. Топ IP-адресов по количеству запросов
SELECT 
    ip,
    COUNT(*) AS requests_count
FROM processed_logs
GROUP BY ip
ORDER BY requests_count DESC
LIMIT 10;

-- 5. Распределение HTTP-методов
SELECT 
    method,
    COUNT(*) AS requests_count
FROM processed_logs
GROUP BY method
ORDER BY requests_count DESC;
