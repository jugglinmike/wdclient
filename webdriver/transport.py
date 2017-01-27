# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import httplib
import json
import urlparse
from result import Result

HTTP_TIMEOUT = 5


class HTTPWireProtocol(object):
    """Transports messages (commands and responses) over the WebDriver
    wire protocol.
    """

    def __init__(self, host, port, url_prefix="/", timeout=HTTP_TIMEOUT):
        """Construct interface for communicating with the remote server.

        :param url: URL of remote WebDriver server.
        :param wait: Duration to wait for remote to appear.
        """

        self.host = host
        self.port = port
        self.url_prefix = url_prefix

        self._timeout = timeout

    def url(self, suffix):
        return urlparse.urljoin(self.path_prefix, suffix)

    def send(self, method, url, body=None, headers=None):
        """Send a command to the remote.

        :param method: "POST" or "GET".
        :param url: "command part" of the requests URL path
        :param body: Body of the request.  Defaults to an empty dictionary
            if ``method`` is "POST".
        :param headers: Additional headers to include in the request.
        """

        if body is None and method == "POST":
            body = {}

        if isinstance(body, dict):
            body = json.dumps(body)

        if isinstance(body, unicode):
            body = body.encode("utf-8")

        if headers is None:
            headers = {}

        url = self.url_prefix + url

        conn = httplib.HTTPConnection(
            self.host, self.port, strict=True, timeout=self._timeout)
        conn.request(method, url, body, headers)

        try:
            resp = conn.getresponse()
            result = Result(resp)
        finally:
            conn.close()

        return result
