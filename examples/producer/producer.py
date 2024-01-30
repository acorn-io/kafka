from kafka import KafkaProducer
import pycountry
import random
import time
import os

bootstrap_servers = f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}"
topic = os.environ['KAFKA_TOPIC']
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Get total number of countries
total_countries = len(pycountry.countries)

# Generate a dummy messsage every second
while True:        
    # Get a random country
    random_index = random.randint(0, total_countries-1) 
    country = list(pycountry.countries)[random_index]

    # Define key and value
    key = country.alpha_2.encode('utf-8')
    value = "alpha_3: {}, name: {}, numeric: {}".format(country.alpha_3, country.name, country.numeric).encode('utf-8')

    # Sent message
    try:
        producer.send(topic, key=key, value=value)
        print("message sent => key:[{}] value:[{}]".format(key, value))
        time.sleep(1)
    except Exception as e:
        print(f"Error sending message: {e}")