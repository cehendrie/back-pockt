import json
import logging

import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AccessToken(object):

    def __init__(self, customer_key, request_token):
        self.customer_key = customer_key
        self.request_token = request_token

    def retrieve(self):
        rt = self.request_token.retrieve()

        url = 'https://getpocket.com/v3/oauth/authorize'
        headers = {
            'X-Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF8'}
        payload = {
            'consumer_key': self.customer_key,
            'code': rt}
        r = requests.post(url, headers=headers, data=json.dumps(payload))

        j = r.json()

        logger.info("access_token: {}".format(j['access_token']))

        return j['access_token']
