import pytest
from ertapi.ensemble import Ensembles


def test_ensembles_names(mock_requests_handler):
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    request_handler = mock_requests_handler

    ens = Ensembles(request_handler=request_handler, metadata_dict=url)
    assert ens.names == ["default", "default_smoother_update"]


def test_ensemble_api(mock_requests_handler):
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    request_handler = mock_requests_handler

    ens_default = Ensembles(request_handler=request_handler, metadata_dict=url)[0]

    assert ens_default.name == "default"
    assert ens_default.parameters.key == [
        "BPR_138_PERSISTENCE",
        "BPR_555_PERSISTENCE",
    ]

    assert ens_default.parameters.group == [
        "SNAKE_OIL_PARAM",
        "SNAKE_OIL_PARAM",
    ]

    assert ens_default.responses.name == [
        "SNAKE_OIL_GPR_DIFF",
        "SNAKE_OIL_OPR_DIFF",
        "SNAKE_OIL_WPR_DIFF",
    ]


def test_parameter_api(mock_requests_handler):
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    requests_handler = mock_requests_handler

    param = Ensembles(request_handler=mock_requests_handler, metadata_dict=url)[
        0
    ].parameters["BPR_138_PERSISTENCE"]
    assert (
        param.metadata["alldata_url"]
        == "http://127.0.0.1:5000/ensembles/1/parameters/1/data"
    )

    assert param.prior["function"] == "UNIFORM"
    assert param.prior["parameter_names"] == ["MIN", "MAX"]
    # needs to be reworked as we want to get (3, 1)
    # issue is only how the mocked data is sent from snake_oil_data
    assert param.data.shape == (1, 3)


def test_realization_api(mock_requests_handler):
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    request_handler = mock_requests_handler

    ens_default = Ensembles(request_handler=request_handler, metadata_dict=url)[0]

    assert ens_default.realizations.name == [0, 1, 2]

    real_0 = ens_default.realizations[0]
    assert real_0.parameters.name == [
        "BPR_138_PERSISTENCE",
        "BPR_555_PERSISTENCE",
        "OP1_DIVERGENCE_SCALE",
    ]

    assert real_0.responses.name == [
        "SNAKE_OIL_GPR_DIFF",
        "SNAKE_OIL_OPR_DIFF",
        "SNAKE_OIL_WPR_DIFF",
    ]
