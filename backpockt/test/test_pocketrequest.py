import requests

from backpockt.accesstoken import AccessToken
from backpockt.pocketrequest import PocketRequest


class TestPocketRequest(object):

    def test_retrieve(self, mocker, monkeypatch):
        mock_access_token = mocker.Mock(AccessToken)
        mock_access_token.retrieve.return_value = 'an_access_token'

        mock_response = mocker.Mock(requests.Response)
        mocker.patch.object(requests, 'get')
        requests.get.return_value = mock_response

        monkeypatch.setattr(mock_response, 'text', 'response_text')

        pocket_request = PocketRequest('a_customer_key', mock_access_token)
        actual = pocket_request.retrieve()

        assert 'response_text' == actual
