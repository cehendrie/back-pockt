import requests
import json

from backpockt.requesttoken import RequestToken
from backpockt.accesstoken import AccessToken


class TestAccessToken(object):
    def test_retrieve(self, mocker):
        mock_request_token = mocker.Mock(RequestToken)
        mock_request_token.retrieve.return_value = 'a_request_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.json.return_value = \
            json.loads("{\"access_token\":\"the_access_token\",\"username\":\"the_username\"}")

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        access_token = AccessToken('a_customer_key', mock_request_token)
        actual = access_token.retrieve()

        assert 'the_access_token' == actual
