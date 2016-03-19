#!/bin/bash
KAFKA_DIR="~/opt/kafka_2.11-0.9.0.1"

gnome-terminal -x sh -c "${KAFKA_DIR}/bin/zookeeper-server-start.sh ${KAFKA_DIR}/config/zookeeper.properties"

gnome-terminal -x sh -c "${KAFKA_DIR}/bin/kafka-server-start.sh ${KAFKA_DIR}/config/server.properties"

gnome-terminal -x sh -c "${KAFKA_DIR}bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test"
