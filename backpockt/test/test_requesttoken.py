import json

import requests

from backpockt.requesttoken import RequestToken


class TestRequestToken(object):
    def test_retrieve(self, mocker):
        mock_response = mocker.Mock(requests.Response)
        mock_response.json.return_value = json.loads("{\"code\":\"the_request_token\",\"state\":null}")

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        request_token = RequestToken('a_customer_key')
        actual = request_token.retrieve()

        assert 'the_request_token' == actual
