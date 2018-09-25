import json

import pytest
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

    def test_retrieve_httperror(self, mocker):
        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        request_token = RequestToken('a_customer_key')

        with pytest.raises(requests.exceptions.HTTPError):
            request_token.retrieve()

    def test_retrieve_connectionerror(self, mocker):
        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.ConnectionError()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        request_token = RequestToken('a_customer_key')

        with pytest.raises(requests.exceptions.ConnectionError):
            request_token.retrieve()

    def test_retrieve_timeout(self, mocker):
        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        request_token = RequestToken('a_customer_key')

        with pytest.raises(requests.exceptions.Timeout):
            request_token.retrieve()

    def test_retrieve_requestexception(self, mocker):
        mock_response = mocker.Mock(requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException()

        mocker.patch.object(requests, 'post')
        requests.post.return_value = mock_response

        request_token = RequestToken('a_customer_key')

        with pytest.raises(requests.exceptions.RequestException):
            request_token.retrieve()
