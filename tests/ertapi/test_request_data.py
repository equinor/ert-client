import pytest
from ertapi.ensemble import RequestData


def test_init_request_data(mock_requests_handler):
    request_handler_mock = mock_requests_handler
    request_data = RequestData(
        request_handler=request_handler_mock,
        metadata_dict={"ref_url": "http://127.0.0.1:5000/ensembles"},
    )

    assert request_data is not None
    assert request_data.data is None
    assert 2 == len(request_data.metadata)
