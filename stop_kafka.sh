#!/bin/bash
KAFKA_DIR="~/opt/kafka_2.11-0.9.0.1"

gnome-terminal -x sh -c "${KAFKA_DIR}/bin/kafka-server-stop.sh"
gnome-terminal -x sh -c "${KAFKA_DIR}/bin/zookeeper-server-stop.sh"
