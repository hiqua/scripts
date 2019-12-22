#!/usr/bin/env python3
import argparse
import datetime
import os
import sys

import requests
from dateutil import parser

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Return 0 if a change occurred less than n minutes ago, 1 otherwise.')
    p.add_argument('-n', '--interval',
                   help='Number of seconds after last event.', default=360)
    args = p.parse_args()
    delay = vars(args)['interval']

    req = {'X-API-Key': os.environ['SYNCTHING_API_KEY']}
    res = requests.get('http://127.0.0.1:8384/rest/events', headers=req)

    d = res.json()

    d = [i for i in d if i['type'] == 'StateChanged'][-1]

    event_time = parser.parse(d['time'])
    current_state = d['data']['to']

    now = datetime.datetime.now(event_time.tzinfo)

    delta = (now - event_time).total_seconds()

    # print(f"Delta is {delta}")
    # print(f"Current state is {current_state}")

    if current_state != 'idle' or delta <= delay:
        sys.exit(0)
    else:
        sys.exit(1)
