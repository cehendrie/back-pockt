import json

import requests


class PocketRequest(object):
    def __init__(self, customer_key, access_token):
        self.customer_key = customer_key
        self.access_token = access_token

    def retrieve(self):
        at = self.access_token.retrieve()
        url = 'https://getpocket.com/v3/get'
        headers = {'Content-Type': 'application/json; charset=UTF8'}
        payload = {
            'consumer_key': self.customer_key,
            'access_token': at,
            'count': '10',
            'detailType': 'complete'}
        r = requests.get(url, headers=headers, data=json.dumps(payload))

        return r.text
