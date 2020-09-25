import ertapi.ensemble
import pandas as pd


class RequestData:
    def __init__(self, request_handler, metadata_dict=None):
        self._metadata = metadata_dict
        self._request_handler = request_handler
        self._clear_data()
        self.load_metadata()

    def _clear_data(self):
        self._realizations = {}
        self._responses = {}
        self._parameters = {}
        self._observations = {}

    def get_node_fields(self, field, key=None):
        if field in self.metadata:
            if key is None:
                return self.metadata[field]
            return [node[key] for node in self.metadata[field]]
        return None

    def realization(self, name):
        if not name in self._realizations:
            for node in self.metadata["realizations"]:
                if name == node["name"]:
                    self._realizations[name] = ertapi.ensemble.Realization(
                        self._request_handler, node
                    )
                    break
        return self._realizations[name]

    def parameter(self, name):
        if not name in self._parameters:
            for node in self.metadata["parameters"]:
                if name == node["key"]:
                    self._parameters[name] = ertapi.ensemble.Parameter(
                        self._request_handler, node
                    )
                    break
        return self._parameters[name]

    def response(self, name):
        if not name in self._responses:
            for node in self.metadata["responses"]:
                if name == node["name"]:
                    self._responses[name] = ertapi.ensemble.Response(
                        self._request_handler, node
                    )
                    break
        return self._responses[name]

    def observation(self, name):
        if not name in self._observations:
            for node in self.metadata["observations"]:
                if name == node["name"]:
                    self._observations[name] = ertapi.ensemble.Observation(
                        self._request_handler, node
                    )
                    break
        return self._observations[name]

    @property
    def parameters(self):
        return self.get_node_fields("parameters", key="key")

    @property
    def responses(self):
        return self.get_node_fields("responses", key="name")

    @property
    def realizations(self):
        return self.get_node_fields("realizations", key="name")

    @property
    def observations(self):
        return self.get_node_fields("observations", key="name")

    @property
    def metadata(self):
        return self._metadata

    @property
    def data(self):
        return self._get_data()

    @property
    def name(self):
        if self.metadata is None or "name" not in self.metadata:
            return None
        return self.metadata["name"]

    def load_metadata(self):
        if self.metadata is not None and "ref_url" in self.metadata:
            self.req_metadata(self.metadata["ref_url"])

    def _get_data(self):
        if "data_url" in self.metadata:
            return self.req_data(self.metadata["data_url"])
        elif "alldata_url" in self.metadata:
            return self.req_alldata(self.metadata["alldata_url"])
        return None

    def req_metadata(self, ref_url):
        _metadata = self._request_handler.request(ref_url=ref_url, json=True)
        if _metadata is not None:
            self._metadata.update(_metadata)

    def req_data(self, ref_url):
        _data = self._request_handler.request(ref_url)
        if _data is not None:
            _data = _data.content.decode()
            return pd.DataFrame([_data.split(",")])

    def req_alldata(self, ref_url):
        _data = self._request_handler.request(ref_url)
        if _data is not None:
            _data = _data.content.decode()
            return pd.DataFrame([x.split(",") for x in _data.split("\n")])
