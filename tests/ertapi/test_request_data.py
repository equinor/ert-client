import pytest
import requests_mock
from tests.ertapi.conftest import mock_urls
from tests.ertapi.snake_oil_data import ensembles_response
from ertapi.ensemble import RequestData
from ertapi.client.request_handler import RequestHandler


class RequestHandlerMock:
    def request(self, ref_url, json=False, stream=False):
        if ref_url in ensembles_response:
            return ensembles_response[ref_url]
        assert True is False


def test_init_request_data():

    request_handler_mock = RequestHandlerMock()
    request_data = RequestData(
        request_handler=request_handler_mock,
        metadata_dict={"ref_url": "http://127.0.0.1:5000/ensembles"},
    )

    assert request_data is not None
    assert request_data.data is None
    assert 2 == len(request_data.metadata)
