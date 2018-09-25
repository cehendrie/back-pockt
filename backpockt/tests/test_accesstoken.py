import json

import pytest
import requests

from backpockt.accesstoken import AccessToken
from backpockt.requesttoken import RequestToken


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

    def test_retrieve_httperror(self, mocker):
        mock_request_token = mocker.Mock(RequestToken)
        mock_request_token.retrieve.return_value = 'a_request_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        access_token = AccessToken('a_customer_key', mock_request_token)

        with pytest.raises(requests.exceptions.HTTPError):
            access_token.retrieve()

    def test_retrieve_connectionerror(self, mocker):
        mock_request_token = mocker.Mock(RequestToken)
        mock_request_token.retrieve.return_value = 'a_request_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.ConnectionError()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        access_token = AccessToken('a_customer_key', mock_request_token)

        with pytest.raises(requests.exceptions.ConnectionError):
            access_token.retrieve()

    def test_retrieve_timeout(self, mocker):
        mock_request_token = mocker.Mock(RequestToken)
        mock_request_token.retrieve.return_value = 'a_request_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        access_token = AccessToken('a_customer_key', mock_request_token)

        with pytest.raises(requests.exceptions.Timeout):
            access_token.retrieve()

    def test_retrieve_requestexception(self, mocker):
        mock_request_token = mocker.Mock(RequestToken)
        mock_request_token.retrieve.return_value = 'a_request_token'

        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        access_token = AccessToken('a_customer_key', mock_request_token)

        with pytest.raises(requests.exceptions.RequestException):
            access_token.retrieve()
