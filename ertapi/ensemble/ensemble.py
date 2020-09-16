from ertapi.ensemble.request_data import RequestData


class Ensemble(RequestData):
    def __init__(self, metadata_dict):
        super().__init__(metadata_dict)
