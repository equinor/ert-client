from ertapi.ensemble.request_data import RequestData


class Response(RequestData):
    def __init__(self, metadata_dict):
        super().__init__(metadata_dict)
