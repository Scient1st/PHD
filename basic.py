import datetime
import json
import logging
import pandas
import urllib2

_BETFAIR_URL = "https://api.betfair.com/exchange/betting/json-rpc/v1"
_TEST_URL = 'http://localhost:8000'

class BetfairApiError(Exception):
    def __init__(self, errordata):
        self.errordata = errordata
        self.exception_name = self.errordata['data']['exceptionname']
        self.error_code = self.errordata['data'][self.exception_name]['errorCode']
        self.error_details = self.errordata['data'][self.exception_name]['errorDetails']
        self.message = '{}: {}. {}'.format(self.exception_name, self.error_code, self.error_details)

    def __str__(self):
        return self.message

def get_headers():
    appkey = open('appkey.delay', 'r').read().strip()
    sessiontoken = open('sessiontoken', 'r').read().strip()
    headers = {'X-Application': appkey, 'X-Authentication': sessiontoken, 'content-type': 'application/json'}
    return headers

_LIVE_SETTINGS = {'url': _BETFAIR_URL, 'headers': get_headers()}
_TEST_SETTINGS = {'url': _TEST_URL, 'headers': get_headers()}

def callAping(data, settings):
    data = json.loads(callAping_raw(request=json.dumps(data), **settings))
    if 'error' in data:
        raise BetfairApiError(data['error'])
    return data

def callAping_raw(url, headers, request):
    try:
        req = urllib2.Request(url, request, headers)
        response = urllib2.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse
    except urllib2.URLError:
        logging.exception('Oops no service available at ' + str(url))

    except urllib2.HTTPError:
        logging.exception('Oops not a valid operation from the service ' + str(url))

def _get_json_query(function_name, params=None):
    if params is None:
        params = {
            "filter": {}
        }
    json_data = {
        "jsonrpc": "2.0",
        "method": "SportsAPING/v1.0/{}".format(function_name),
        "params": params,
        "id": 1
    }
    return json_data

### Implementation of API functions as python functions
def listEventTypes(settings):
    query = _get_json_query('listEventTypes')
    result = callAping(query, settings)
    return pandas.DataFrame([dict(x['eventType'].items() + [('marketCount', x['marketCount'])]) for x in result['result']]).sort_values('marketCount', ascending=False)

def _betfair_date(date):
    '''
    returns the betfair representation of a datetime date object
    '''
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')

def _create_market_filter(**kwargs):
    '''
    MarketFilter objects are used in multiple API functions
    '''
    market_filter = {
        k: v for k,v in kwargs.items()
    }
    return market_filter

def listJustStartedEvents(settings, eventTypeId, timeFrame=30):
    '''
    Returns
    timeFrame in minutes
    '''
    now = datetime.datetime.now()
    time_delta = datetime.timedelta(0, timeFrame*60)
    params = {
        'filter': _create_market_filter(eventTypeIds=[str(eventTypeId)],
                                        marketStartTime={
                                            'from': _betfair_date(now-time_delta),
                                            'to': _betfair_date(now),
                                            'turnInPlayEnabled': True
                                        })
    }
    query = _get_json_query('listEvents', params=params)
    result = callAping(query, settings)
    return result['result']

def listInPlayEvents(settings, eventTypeId):
    '''
    Returns
    timeFrame in minutes
    '''
    now = datetime.datetime.now()
    time_delta = datetime.timedelta(0, 60*60*24*100)
    params = {
        'filter': _create_market_filter(eventTypeIds=[str(eventTypeId)],
                                        marketStartTime={
                                            'from': _betfair_date(now-time_delta),
                                            'to': _betfair_date(now),
                                            'InPlayOnly': True
                                        })
    }
    query = _get_json_query('listEvents', params=params)
    result = callAping(query, settings)
    return result['result']

def getMatchOddsMarket(*eventIds):
    params = {
        'filter': _create_market_filter(
            eventTypeIds=[str(1)],
            eventIds=list(map(str, eventIds)),
            marketTypeCodes=['MATCH_ODDS']
        ),
        'maxResults': len(eventIds)
    }
    query = _get_json_query('listMarketCatalogue', params=params)
    result = callAping(query)
    return result['result']

### DataFrame of all event Types
#event_types_data = listEventTypes()

### All Soccer Events starting in the next 60 minutes
#soccer_events = listEvents(1, timeFrame=60)
#in_play_soccer = listInPlayEvents(1)

def printPrices(marketId):
    params=_create_market_filter(orderProjection='EXECUTABLE', marketIds=[marketId],
                                 priceProjection={"priceData":["EX_BEST_OFFERS"],"virtualise":"true"})
    result = callAping(_get_json_query('listMarketBook', params=params))
    for runner in result['result'][0]['runners']:
        print 'status:', runner['status'], 'price:', runner['lastPriceTraded'],
    print ''

import time
def monitorPrices(marketId):
    while True:
        time.sleep(1)
        printPrices(marketId)
