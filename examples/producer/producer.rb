require 'kafka'
require 'json'

kafka = Kafka.new(
  seed_brokers: ["#{ENV['KAFKA_HOST']}:#{ENV['KAFKA_PORT']}"],
  client_id: 'ruby-producer'
)

producer = kafka.producer

topic = ENV['KAFKA_TOPIC']

# Dummy producer logic: Produce a message every second
loop do
  message = { timestamp: Time.now.to_s, data: 'Dummy message' }.to_json
  producer.produce(message, topic: topic)
  sleep 1
end

at_exit { producer.shutdown }