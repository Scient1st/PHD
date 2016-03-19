#!/bin/bash
KAFKA_DIR="~/opt/kafka_2.11-0.9.0.1"

gnome-terminal -x sh -c "${KAFKA_DIR}/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test"
sleep 1

gnome-terminal -x sh -c "${KAFKA_DIR}/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test"
