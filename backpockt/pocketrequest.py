import json
import logging

import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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

        try:
            r = requests.get(url, headers=headers, data=json.dumps(payload))
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Http Error:", err)
            logger.error("http error: {}".format(err))
            raise err
        except requests.exceptions.ConnectionError as err:
            print("Error Connecting:", err)
            logger.error("connection error: {}".format(err))
            raise err
        except requests.exceptions.Timeout as err:
            print("Timeout Error:", err)
            logger.error("timeout: {}".format(err))
            raise err
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            logger.error("request error: {}".format(err))
            raise err

        logger.info("response text: {}".format(r.text))

        return r.text
