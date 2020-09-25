from ertapi.ensemble import RequestData, Ensemble
from ertapi.client.request_handler import RequestHandler


class Ensembles(RequestData):
    def __init__(self, request_handler, metadata_dict):
        super().__init__(request_handler=request_handler, metadata_dict=metadata_dict)
        self._ensembles = {}

    def __getitem__(self, ens_id):
        return self._get_ensemble_by_id(ens_id)

    def __iter___(self):
        return self._ensembles

    def __len__(self):
        return len(self._ensembles)

    def _get_ensemble_by_id(self, ens_id):
        if not ens_id in self._ensembles:
            self._ensembles[ens_id] = Ensemble(
                request_handler=self._request_handler,
                metadata_dict=self.metadata["ensembles"][ens_id],
            )
        return self._ensembles[ens_id]

    @property
    def names(self):
        return self.get_node_fields("ensembles", key="name")

    @property
    def times_created(self):
        return self.get_node_fields("ensembles", key="time_created")

    @property
    def ensembles(self):
        return self._ensembles


if __name__ == "__main__":
    url = {"ref_url": "http://127.0.0.1:5000/ensembles"}
    request_handler = RequestHandler()
    ens = Ensembles(request_handler=request_handler, metadata_dict=url)
    bpr_data = ens[0].parameter("BPR_138_PERSISTENCE").data
    print(bpr_data.shape)

    print(ens.times_created)
    print(ens[0].responses)
    print(ens[0].response("POLY_RES").observation("POLY_OBS").name)
    print(ens[0].response("POLY_RES").observation("POLY_OBS").values.data)
    print(ens[0].realization(0).response("POLY_RES").data)
    print(ens[0].response("POLY_RES").realization(0).univariate_misfits("POLY_OBS"))
    print(ens[0].response("POLY_RES").data)
    print(ens[0].parameter("COEFF_A").data)
