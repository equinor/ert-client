import pytest
import json
from tests.ertapi.snake_oil_data import ensembles_response


@pytest.fixture
def mock_urls(requests_mock):
    mock = requests_mock
    for ref_url in ensembles_response:
        mock.register_uri("GET", ref_url, text=json.dumps(ensembles_response[ref_url]))
