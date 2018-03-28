from __future__ import absolute_import, print_function, unicode_literals

from requests.auth import HTTPBasicAuth

from .client import Client


class UserClient(Client):
    def auth(self, un, pw):
        """
        Authorise client with provided credentials. Does not check with Sync
        Gateway that credentials are correct until a request is made.

        Args:
            un (str): User name.
            pw (str): Password.

        Returns:
            None
        """
        self._auth = HTTPBasicAuth(un, pw)
