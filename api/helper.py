
class ApiHelper():

    def prepare_url(self, endpoint: str, params: dict) -> str:
        if len(params) > 0:
            endpoint = endpoint + "?"
        else:
            return endpoint

        for key in params:
            endpoint = endpoint + key + "=" + params[key] + "&"

        return endpoint[:-1]

