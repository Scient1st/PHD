'''
Kafka publisher that reads the list of soccer events from BF and publishes them one by one
'''

import argparse
import datetime
import json

from kafka import KafkaProducer

import basic

def listEvents(settings, eventTypeId, n):
    '''
    Returns all events that will turn inPlay in the next n minutes
    '''
    now = datetime.datetime.now()
    time_delta = datetime.timedelta(0, n*60)
    params = {
        'filter': basic._create_market_filter(eventTypeIds=[str(eventTypeId)],
                                              marketStartTime={
                                                  'from': basic._betfair_date(now-time_delta),
                                                  'to': basic._betfair_date(now),
                                                  'InPlayOnly': True
                                              })
    }
    query = basic._get_json_query('listEvents', params=params)
    result = basic.callAping(query, settings)
    return result['result']

def run(eventTypeId, frequency, producer, topic):
    settings = basic._TEST_SETTINGS
    events = listEvents(settings, eventTypeId, frequency)
    for event in events:
        producer.send(topic, event)
    producer.flush()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frequency', help='How many minutes into the future?', default=60, type=int)
    parser.add_argument('--eventTypeId', help='Event Type Id', type=int, default=1)
    parser.add_argument('--bootstrap-servers', default='localhost:9092', type=str)
    parser.add_argument('--topic', default='test', type=str)
    args = parser.parse_args()
    producer = KafkaProducer(bootstrap_servers=args.bootstrap_servers, value_serializer=json.dumps)
    run(args.eventTypeId, args.frequency, producer, args.topic)

if __name__=='__main__':
    main()
