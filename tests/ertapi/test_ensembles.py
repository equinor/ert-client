import pytest
import requests_mock
from tests.ertapi.conftest import mock_urls

from ertapi.ensemble import Ensembles
from ertapi.client.request_handler import RequestHandler


def test_ensembles_names(mock_urls):
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    request_handler = RequestHandler()
    ens = Ensembles(request_handler=request_handler, metadata_dict=url)
    assert ens.names == ["default", "default_smoother_update"]


def test_ensemble_api(mock_urls):
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    request_handler = RequestHandler()
    ens = Ensembles(request_handler=request_handler, metadata_dict=url)

    assert ens[0].name == "default"
    assert ens[0].parameters == [
        "BPR_138_PERSISTENCE",
        "BPR_555_PERSISTENCE",
    ]
    assert (
        ens[0].parameter("BPR_138_PERSISTENCE").metadata["alldata_url"]
        == "http://127.0.0.1:5000/ensembles/1/parameters/1/data"
    )


# data tests should be thought to be mocked differently
def test_response_data_api(mock_urls):
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    request_handler = RequestHandler()
    ens = Ensembles(request_handler=request_handler, metadata_dict=url)
    bpr_data = ens[0].parameter("BPR_138_PERSISTENCE").data
    print(ens[0].responses)
    assert ens[0].responses == [
        "SNAKE_OIL_GPR_DIFF",
        "SNAKE_OIL_OPR_DIFF",
        "SNAKE_OIL_WPR_DIFF",
    ]
    # needs to be reworked as we want to get (3, 1)
    # issue is only how the mocked data is sent from snake_oil_data
    assert bpr_data.shape == (1, 3)
