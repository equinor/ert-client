from typing import List

import pytest


class ParameterDefinition:
    name = ""
    group = ""
    function = ""
    arguments = []
    argument_values = []


class ParameterSample:
    def __init__(self, ref, value):
        self.parameter_definition_ref: ParameterDefinition = ref
        self.parameter_value: float = value


class Realization:
    def __init__(self, name):
        self.name = name
        self.parameter_samples: List[ParameterSample] = []
        self.responses = {}


class Ensemble:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.parameters: List[ParameterDefinition] = []
        self.realizations: List[Realization] = []


class Ensembles:
    ensemble_list = []

    @property
    def names(self):
        return [e.name for e in self.ensemble_list]

    def __getitem__(self, item) -> Ensemble:
        for e in self.ensemble_list:
            if e.name == item:
                return e
        raise KeyError

    def __contains__(self, item):
        try:
            return self[item] is not None
        except KeyError:
            return False


@pytest.fixture()
def ensembles():
    print("setup")

    ensembles = Ensembles()

    bpr_138 = ParameterDefinition()
    bpr_138.group = "SNAKE_OIL_PARAM"
    bpr_138.name = "BPR_138_PERSISTENCE"
    bpr_138.function = "UNIFORM"
    bpr_138.arguments = ["MIN", "MAX"]
    bpr_138.argument_values = [0.2, 0.7]

    bpr_155 = ParameterDefinition()
    bpr_155.group = "SNAKE_OIL_PARAM"
    bpr_155.name = "BPR_155_PERSISTENCE"
    bpr_155.function = "UNIFORM"
    bpr_155.arguments = ["MIN", "MAX"]
    bpr_155.argument_values = [0.1, 0.5]

    r1 = Realization(name="1")
    r1.parameter_samples.append(ParameterSample(bpr_138, value=0.5))
    r1.parameter_samples.append(ParameterSample(bpr_155, value=0.17))
    r1.responses["FOPR"] = [0.5, 0.7, 0.2, 0.4]
    r1.responses["WOPR"] = [0.7, 0.2, 0.1, 0.23]

    r2 = Realization(name="2")
    r2.parameter_samples.append(ParameterSample(bpr_138, value=0.63))
    r2.parameter_samples.append(ParameterSample(bpr_155, value=0.2))
    r2.responses["FOPR"] = [0.4, 0.5, 0.54, 0.3]
    r2.responses["WOPR"] = [0.6, 0.4, 0.2, 0.23]

    r3 = Realization(name="3")
    r3.parameter_samples.append(ParameterSample(bpr_138, value=0.73))
    r3.parameter_samples.append(ParameterSample(bpr_155, value=0.22))
    r3.responses["FOPR"] = [0.45, 0.55, 0.55, 0.35]
    r3.responses["WOPR"] = [0.65, 0.45, 0.25, 0.25]

    ensemble = Ensemble("default")
    ensemble.parameters = [bpr_138, bpr_155]
    ensemble.realizations.extend([r1, r2, r3])

    ensembles.ensemble_list.append(ensemble)

    ens_2 = Ensemble("default_smoother_update", ensemble)
    ensembles.ensemble_list.append(ens_2)
    ens_3 = Ensemble("default_smoother_update_update", ens_2)
    ensembles.ensemble_list.append(ens_3)

    yield ensembles


def test_ensembles(ensembles: Ensembles):
    ens_1 = ensembles["default"]
    assert ens_1 == ensembles.ensemble_list[0]
    assert ens_1.parent is None

    assert "default_smoother_update" in ensembles
    assert ensembles.names == [
        "default",
        "default_smoother_update",
        "default_smoother_update_update",
    ]

    ens_2 = ensembles["default_smoother_update"]
    assert ens_2.parent == ens_1
    ens_3 = ensembles["default_smoother_update_update"]
    assert ens_3.parent == ens_2


def test_parameters(ensembles: Ensembles):
    ens_1 = ensembles["default"]
    assert len(ens_1.parameters) == 2

    p1 = ens_1.parameters[0]
    assert p1.group == "SNAKE_OIL_PARAM"
    assert p1.name == "BPR_138_PERSISTENCE"
    assert p1.function == "UNIFORM"
    assert p1.arguments == ["MIN", "MAX"]
    assert p1.argument_values == [0.2, 0.7]


def test_realizations(ensembles: Ensembles):
    ens_1 = ensembles["default"]
    assert len(ens_1.realizations) == 3

    p1 = ens_1.parameters[0]
    r2 = ens_1.realizations[1]
    assert r2.name == "2"
    assert r2.parameter_samples[0].parameter_definition_ref == p1
    assert r2.parameter_samples[0].parameter_value == 0.63

    assert "FOPR" in r2.responses
    assert r2.responses["FOPR"] == [0.4, 0.5, 0.54, 0.3]
