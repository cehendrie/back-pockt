import json
import logging

import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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

        try:
            r = requests.post(url, headers=headers, data=json.dumps(payload))
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

        j = r.json()

        logger.info("request_token: {}".format(j['code']))

        return j['code']
