import pytest
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

    def test_retrieve_httperror(self, mocker):
        mock_access_token = mocker.Mock(AccessToken)
        mock_access_token.retrieve.return_value = 'an_access_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mocker.patch.object(requests, 'get')
        requests.get.return_value = mock_response

        pocket_request = PocketRequest('a_customer_key', mock_access_token)

        with pytest.raises(requests.exceptions.HTTPError):
            pocket_request.retrieve()

    def test_retrieve_connectionerror(self, mocker):
        mock_access_token = mocker.Mock(AccessToken)
        mock_access_token.retrieve.return_value = 'an_access_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.ConnectionError()

        mocker.patch.object(requests, 'get')
        requests.get.return_value = mock_response

        pocket_request = PocketRequest('a_customer_key', mock_access_token)

        with pytest.raises(requests.exceptions.ConnectionError):
            pocket_request.retrieve()

    def test_retrieve_timeout(self, mocker):
        mock_access_token = mocker.Mock(AccessToken)
        mock_access_token.retrieve.return_value = 'an_access_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()

        mocker.patch.object(requests, 'get')
        requests.get.return_value = mock_response

        pocket_request = PocketRequest('a_customer_key', mock_access_token)

        with pytest.raises(requests.exceptions.Timeout):
            pocket_request.retrieve()

    def test_retrieve_requestexception(self, mocker):
        mock_access_token = mocker.Mock(AccessToken)
        mock_access_token.retrieve.return_value = 'an_access_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException()

        mocker.patch.object(requests, 'get')
        requests.get.return_value = mock_response

        pocket_request = PocketRequest('a_customer_key', mock_access_token)

        with pytest.raises(requests.exceptions.RequestException):
            pocket_request.retrieve()
