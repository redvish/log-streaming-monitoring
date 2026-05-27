import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

ips = ['192.168.1.10', '192.168.1.11', '192.168.1.12']
methods = ['GET', 'POST', 'PUT', 'DELETE']
urls = ['/api/users', '/api/login', '/api/orders']
status_codes = [200, 201, 401, 403, 404, 500]
user_agents = ['Mozilla/5.0', 'curl/7.68.0', 'PostmanRuntime/7.28.4']

try:
    while True:
        log = {
            'ip': random.choice(ips),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'method': random.choice(methods),
            'url': random.choice(urls),
            'status_code': random.choice(status_codes),
            'response_size': random.randint(100, 5000),
            'user_agent': random.choice(user_agents)
        }
        producer.send('web_logs', log)
        print(f"Sent: {log}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Producer stopped")
    producer.close()
