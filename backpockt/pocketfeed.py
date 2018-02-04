import json


class PocketFeed(object):
    def __init__(self, request):
        self.request = request

    def process(self):
        request_text = self.request.retrieve()
        j = json.loads(request_text)
        for article in list(j["list"].values()):
            print("article.given_url: {}".format(article["given_url"]))
