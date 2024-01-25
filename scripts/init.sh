#!/bin/sh
# set -euxo pipefail

# Make sure this script is only triggered on Acorn creation events
echo "event: ${ACORN_EVENT}"
if [ "${ACORN_EVENT}" = "delete" ]; then
   echo "ACORN_EVENT must be [create, update], currently is [${ACORN_EVENT}]"
   exit 0
fi

# Couple of variables to make local testing simpler
termination_log="/dev/termination-log"
acorn_output="/run/secrets/output"

# Target kafka container
KAFKA_HOST="kafka"
KAFKA_PORT="9092"

# Wait for kafka to be available
until kafka-topics.sh --list --bootstrap-server $KAFKA_HOST:$KAFKA_PORT; do
    echo "Waiting for Kafka to be available..."
    sleep 5
done

# Create the topic if not exist yet (check needed in case the setup job is run several times)
echo "#############################"
kafka-topics.sh --list --bootstrap-server $KAFKA_HOST:$KAFKA_PORT
kafka-topics.sh --list --bootstrap-server $KAFKA_HOST:$KAFKA_PORT | grep $TOPIC
echo "#############################"

topic_exists=$(kafka-topics.sh --list --bootstrap-server $KAFKA_HOST:$KAFKA_PORT | grep $TOPIC)
if [ "$topic_exists" != "" ]; then
    echo "Topic [$TOPIC] already exists"
else 
    res=$(kafka-topics.sh --create --topic $TOPIC --bootstrap-server $KAFKA_HOST:$KAFKA_PORT >/dev/null 2>&1)
    if [ $? -eq 0 ]; then
        echo "Topic [$TOPIC] created"
    else
        echo "topic cannot be created"
        echo $res | tee ${termination_log}
        exit 1
    fi
fi

echo "Kafka server has been initialized and configured!"

# Define service
cat > $acorn_output<<EOF
services: broker: {
    default: true
    container: "kafka"
    ports: "9092"
    data: {
        topicName: "${TOPIC}"
    }
}
EOF