import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PocketFeed(object):
    def __init__(self, request):
        self.request = request

    def process(self):
        request_text = self.request.retrieve()
        j = json.loads(request_text)
        for article in list(j["list"].values()):
            print("article.given_url: {}".format(article["given_url"]))
            logger.debug("article.given_url: {}".format(article["given_url"]))
