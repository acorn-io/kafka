from kafka import KafkaConsumer
import os

consumer = KafkaConsumer(
    os.environ['KAFKA_TOPIC'],
    bootstrap_servers=f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
    group_id='python-consumer',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8')
)

# Consumer logic: Write each received message to standard output
for message in consumer:
    print(f"Received message: {message.value}")
