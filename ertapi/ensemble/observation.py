from ertapi.ensemble.request_data import RequestData


class ObsParam(RequestData):
    def __init__(self, metadata_dict):
        super().__init__(metadata_dict)


params_keys = ["active_mask", "data_indexes", "key_indexes", "std", "values"]


class Observation(RequestData):
    def __init__(self, metadata_dict):
        super().__init__(metadata_dict)

    def load_metadata(self):
        super().load_metadata()

        self._obs_params = {
            key: ObsParam(self.metadata["data"][key]) for key in params_keys
        }

    @property
    def active_mask(self):
        return self._obs_params["active_mask"]

    @property
    def data_indexes(self):
        return self._obs_params["data_indexes"]

    @property
    def key_indexes(self):
        return self._obs_params["key_indexes"]

    @property
    def std(self):
        return self._obs_params["std"]

    @property
    def values(self):
        return self._obs_params["values"]
