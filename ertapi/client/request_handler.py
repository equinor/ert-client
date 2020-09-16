import requests


class RequestHandler:
    @staticmethod
    def request(ref_url, stream=False):
        reply = None
        try:
            reply = requests.get(ref_url, stream=stream)
        except requests.ConnectionError:
            return None
        if reply.status_code == 200:
            return reply
        return None
