from __future__ import absolute_import, print_function, unicode_literals

from requests import delete, get, put

from .database import Database
from .helpers import ComparableMixin, sg_method


class Client(ComparableMixin, object):
    """
    Abstract parent class for `AdminClient` and `UserClient`.

    Attributes:
        _auth (requests.HTTPBasicAuth): Initialises to `None` and is only used
            by `UserClient`.
        url (str): Sync Gateway REST API URL.
    """
    CREATED = 1
    UPDATED = 2
    CONFLICT = 3

    def __init__(self, url):
        """
        Args:
            url (str): Sync Gateway REST API URL (excluding database but
                including trailing slash).
        """
        self.url = url
        self._auth = None

    def get_server(self):
        """
        Returns:
            dict: Meta-information about the server.
        """
        return self.get(self.url).json()

    def get_database(self, database_name):
        """
        Get a `Database` instance connected to this client.

        Args:
            database_name (str): Name of database.

        Returns:
            Database
        """
        return Database(self, database_name)

    # --- REST Verbs ---

    @sg_method
    def get(self, url, **kwargs):
        if self._auth:
            kwargs['auth'] = self._auth
        return get(url, **kwargs)

    @sg_method
    def put(self, url, data):
        return put(url, json=data)

    @sg_method
    def delete(self, url, **kwargs):
        return delete(url, **kwargs)
