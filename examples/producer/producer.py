from kafka import KafkaProducer
from faker import Faker
import pycountry
import random
import time
import os

bootstrap_servers = f"{os.environ['KAFKA_HOST']}:{os.environ['KAFKA_PORT']}"
topic = os.environ['KAFKA_TOPIC']
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Set up Faker to generate country-related data
fake = Faker()

total_countries = len(pycountry.countries)

# Generate a dummy messsage every second
while True:
    # Get random country code and related name
    country_code = fake.country_code()
    country_description = fake.country()
    
    # Convert to bytes
    key = country_code.encode('utf-8')
    value = country_description.encode('utf-8')
        
    random_index = random.randint(0, total_countries) 
    country = list(pycountry.countries)[random_index]
    print(country)

    value = "alpha_2: {}, alpha_3: {}, name: {}, numeric: {}".format(country.alpha_2, country.alpha_3, country.name, country.numeric).encode('utf-8')

    # Sent message
    try:
        producer.send(topic, key=key, value=value)
        print("message sent => key:[{}] value:[{}]".format(key, value))
        time.sleep(1)
    except Exception as e:
        print(f"Error sending message: {e}")