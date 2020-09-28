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
        raise Exception("ref_url {} is not supported from the mock".format(ref_url))


def test_request_data_ensembles():

    ref_url_key = "ref_url"
    ref_url_value = "http://127.0.0.1:5000/ensembles"
    request_handler_mock = RequestHandlerMock()
    request_data = RequestData(
        request_handler=request_handler_mock,
        metadata_dict={ref_url_key: ref_url_value},
    )

    assert request_data is not None
    assert request_data.name is None
    assert request_data.data is None
    assert 2 == len(request_data.metadata)
    assert request_data.metadata[ref_url_key] == ref_url_value
    assert 2 == len(request_data.metadata["ensembles"])


def test_request_data_ensemble():
    ref_url_key = "ref_url"
    ref_url_value = "http://127.0.0.1:5000/ensembles/1"
    request_handler_mock = RequestHandlerMock()
    request_data = RequestData(
        request_handler=request_handler_mock,
        metadata_dict={ref_url_key: ref_url_value},
    )

    assert request_data is not None
    assert request_data.name == "default"
    assert request_data.data is None
    assert 8 == len(request_data.metadata)

    assert request_data.metadata[ref_url_key] == ref_url_value

    assert 1 == len(request_data.metadata["children"])

    assert 2 == len(request_data.parameters)
    assert request_data.parameters[0] == "BPR_138_PERSISTENCE"
    assert request_data.parameters[1] == "BPR_555_PERSISTENCE"

    assert 3 == len(request_data.realizations)
    assert request_data.realizations[0] == 0
    assert request_data.realizations[1] == 1
    assert request_data.realizations[2] == 2

    assert 3 == len(request_data.responses)
    assert request_data.responses[0] == "SNAKE_OIL_GPR_DIFF"
    assert request_data.responses[1] == "SNAKE_OIL_OPR_DIFF"
    assert request_data.responses[2] == "SNAKE_OIL_WPR_DIFF"
