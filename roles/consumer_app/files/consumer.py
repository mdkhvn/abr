from kafka import KafkaConsumer
import psycopg2
import json
import traceback

print("Starting Kafka consumer...")

consumer = KafkaConsumer(
    'mysql-errors',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: m.decode('utf-8'),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)
print("Connecting to PostgreSQL...")

conn = psycopg2.connect(
    dbname='mysql_logs',
    user='mysql_logger',
    password='HalfOfbl00d!@',
    host='localhost'
)
cur = conn.cursor()

for msg in consumer:
    try:
        cur.execute(
            "INSERT INTO mysql_logs(log_time, host, severity, message) VALUES (NOW(), %s, %s, %s)",
            ('mysql1', 'INFO', msg.value)
        )
        conn.commit()
        print("Inserted:", msg.value)
    except Exception as e:
        print("DB ERROR:", e)
        print(traceback.format_exc())
        conn.rollback()