from kafka import KafkaConsumer
import os

consumer = None
try:
    consumer = KafkaConsumer(
        os.environ['KAFKA_TOPIC'],
        bootstrap_servers=f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}",
        auto_offset_reset='earliest',
        enable_auto_commit=True,  # Disable auto-commit
        value_deserializer=lambda x: x.decode('utf-8')
    )
except Exception as e:
    print(f"Error initializing Kafka consumer: {e}")

print("Consumer started")

# Consumer logic: Write each received message to standard output
for message in consumer:
    print ("Received message => %s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                              message.offset, message.key,
                                                              message.value))