import json

class Result():
    def __init__(self, response):
        self.status = response.status
        self.body = response.read()

        if self.body:
            self.body = json.loads(self.body)

        self._validate(response)

    def __str__(self):
        return 'Result(status=%d, body=%s)' % self.status, self.body

    # SpecID: dfn-send-a-response
    def _validate(self, response):
        # > 3. Set the response's header with name and value with the following
        # >    values:
        # >
        # >    "Content-Type"
        # >       "application/json; charset=utf-8"
        # >    "cache-control"
        # >       "no-cache"
        assert response.getheader("Content-Type") == "application/json; charset=utf-8"
        assert response.getheader("cache-control") == "no-cache"

        # > 4. If data is not null, let response's body be a JSON Object with a
        #      key value set to the JSON Serialization of data.
        if self.body:
            assert "value" in self.body
