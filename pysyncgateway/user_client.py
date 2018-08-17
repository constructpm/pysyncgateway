from __future__ import absolute_import, print_function, unicode_literals

from requests.auth import HTTPBasicAuth

from .client import Client


class UserClient(Client):
    def auth(self, username, password):
        """
        Authorise client with provided credentials. Does not check with Sync
        Gateway that credentials are correct until a request is made.

        Args:
            username (str): User name.
            password (str): Password.

        Returns:
            None
        """
        self._auth = HTTPBasicAuth(username, password)
