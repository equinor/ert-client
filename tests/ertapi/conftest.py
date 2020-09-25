from ertapi.ensemble import request_data
import pytest
import json
from tests.ertapi.snake_oil_data import ensembles_response


class RequestHandlerMock:
    def request(self, ref_url, json=False, stream=False):
        if ref_url in ensembles_response:
            return ensembles_response[ref_url]
        assert True is False


@pytest.fixture
def mock_requests_handler():
    return RequestHandlerMock()
