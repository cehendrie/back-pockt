import json

import requests


class RequestToken(object):

    def __init__(self, customer_key):
        """
        :param customer_key:
        """
        self.custom_key = customer_key

    def retrieve(self):
        """
        Retrieve a Pocket API request token for a customer key.
        :return: Pocket API request token
        """
        url = 'https://getpocket.com/v3/oauth/request'
        headers = {
            'X-Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF8'}
        payload = {
            'consumer_key': self.custom_key,
            'redirect_uri': 'back-pocket:authorizationFinished'}
        r = requests.post(url, headers=headers, data=json.dumps(payload))

        j = r.json()

        return j['code']
