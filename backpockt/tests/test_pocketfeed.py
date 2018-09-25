from backpockt.pocketfeed import PocketFeed
from backpockt.pocketrequest import PocketRequest


class TestPocketFeed(object):
    def test_process(self, mocker):
        mock_pocket_request = mocker.Mock(PocketRequest)
        mock_pocket_request.retrieve.return_value = \
            '{\"list\": {' \
            '\"1\": {\"given_url\": \"http://test_id_1.com\"}, ' \
            '\"2\": {\"given_url\": \"http://test_id_2.com\"}}}'

        pocket_feed = PocketFeed(mock_pocket_request)
        pocket_feed.process()

        assert True
