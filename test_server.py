'''
Imitate a betfair server for testing
'''

import argparse
import BaseHTTPServer
import json
import logging

def authenticate(headers):
    if 'X-Authentication' not in headers:
        data = {'errorcode': -1, 'message': 'No X-Authentication Available'}
        return -1
    return 0

def validate_input_data(input_data):
    assert input_data['jsonrpc'] == '2.0'
    sportsAping, _, function_name = input_data['method'].rpartition('/')
    assert sportsAping == r'SportsAPING/v1.0'
    return function_name, input_data['params']

def listEventTypes(filter=None, locale=None):
    all_event_types = [{'eventType': {'id': 1, 'name': 'Soccer'}, 'marketCount': 1000}]
    return all_event_types

def listEvents(filter=None, locale=None):
    all_events = [{
        'event': {
            'id': 1010,
            'name': 'ManU vs Leicester',
            'countryCode': 'UK',
            'timezone': 'GMT',
            'venue': 'Manchester',
            'openDate': '2015-01-01'
        },
        'marketCount': 10
    }]
    return all_events

_FUNCTIONS = {
    'listEventTypes': listEventTypes,
    'listEvents': listEvents
}

class BetfairRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        if authenticate(self.headers)<0:
            return
        logging.info('calling GET with path ' + self.path)
        data = {
            'server': 'Betfair',
            'result': 'ok'
        }
        self.wfile.write(json.dumps(data))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        data = {'errorcode': -17, 'message': 'No idea what happened'}
        try:
            authenticate(self.headers)
            logging.info('Calling POST at path ' + self.path)
            input_data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            logging.info('Calling POST with input data ' + str(input_data))
            function_name, params = validate_input_data(input_data)
            data = _FUNCTIONS[function_name](**params)
            self.wfile.write(json.dumps({'result': data}))
        except:
            logging.exception('Exception caught while reading message')
            self.wfile.write(json.dumps(data))

def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=BetfairRequestHandler,
        port=8000):
    server_address = ('localhost', port)
    logging.info('starting server at {}:{}'.format(*server_address))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Basic test server for the BF API')
    parser.add_argument('--port', default=8000, type=int, help='Port for the server. Defaults to 8000.')
    args = parser.parse_args()
    run(port=args.port)

if __name__=='__main__':
    main()
