#!/usr/bin/python
# Pushbullet notification connector
# Author: skorov

import requests
import json


def push(message, apikey):
    try:
        url = "https://api.pushbullet.com/v2/pushes"
        params = {'type': 'note', 'title': 'Subdomainator', 'body': message}
        headers = {'Access-Token': apikey, 'Content-Type': 'application/json'}
        requests.post(url, data=json.dumps(params), headers=headers)
    except Exception as e:
        print(str(e))
