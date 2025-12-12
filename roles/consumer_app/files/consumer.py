from kafka import KafkaConsumer
import psycopg2
import json

consumer = KafkaConsumer(
    'mysql-logs',
    bootstrap_servers=['192.168.1.17:9092'],
    value_deserializer=lambda m: m.decode('utf-8'),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

conn = psycopg2.connect(
    dbname='mysql_logs',
    user='mysql_logger',
    password='HalfOfbl00d!@',
    host='localhost'
)
cur = conn.cursor()

for msg in consumer:
    cur.execute(
        "INSERT INTO mysql_logs(log_time, host, severity, message) VALUES (NOW(), %s, %s, %s)",
        ('mysql1', 'INFO', msg.value)
    )
    conn.commit()
