#!/usr/bin/env python3
from pprint import pprint
import json
import requests
import os

if __name__ == '__main__':

    req = {'X-API-Key': os.environ['SYNCTHING_API_KEY']}
    res = requests.get('http://127.0.0.1:8384/rest/events', headers=req)

    d = res.json()

    d = (i for i in d if i['type'] == 'StateChanged')

    for e in d:
        if e['data']['to'] not in ('idle', 'scanning', 'scan-waiting',
                                   'syncing'):
            print("Something weird going on!")
            pprint(e)
