'''
A Kafka publisher that sends a heartbeat at constant time intervals
'''

import argparse
import datetime
import time
from kafka import KafkaProducer

def time_loop(sleep_interval, producer, topic):
    while True:
        now = b'{}'.format(datetime.datetime.now())
        producer.send(topic, value=now)
        time.sleep(sleep_interval)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frequency', help='frequency in seconds', type=float, default=1.0)
    parser.add_argument('--bootstrap-servers', default='localhost:9092', type=str)
    parser.add_argument('--topic', default='test', type=str)
    args = parser.parse_args()
    producer = KafkaProducer(bootstrap_servers=args.bootstrap_servers)
    time_loop(args.frequency, producer, args.topic)

if __name__=='__main__':
    main()
