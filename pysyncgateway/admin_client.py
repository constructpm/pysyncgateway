from __future__ import absolute_import, print_function, unicode_literals

from requests import delete, get, put

from .database import Database
from .helpers import ComparableMixin, sg_method


class AdminClient(object, ComparableMixin):
    """
    SyncGateway client for performing admin actions on the private admin port.
    This client is hardened to handle the Sync Gateway endpoint not being
    available - for example if Couchbase is being restarted.

    Attributes:
        url (str): URL of admin port.
    """

    def __init__(self, url):
        """
        Args:
            url (str): Pass base Sync Gateway URL (excluding database but
                including trailing slash) for this instance to connect to.
        """
        self.url = url

    def __repr__(self):
        return '<AdminClient on "{url}">'.format(url=self.url)

    def __lt__(self, other):
        """
        Two AdminClient instances are the same if they are both talking to the
        same URL (there is no username / password to distinguish them).

        Returns:
            bool

        Raises:
            AssertionError: When `other` is not an AdminClient.
        """
        assert isinstance(other, AdminClient)
        return self.url < other.url

    def get_server(self):
        """
        Returns:
            dict: Meta-information about the server.
        """
        return self.get(self.url).json()

    # --- Databases ---

    def get_database(self, database_name):
        """
        Get a `Database` instance connected to this client

        Args:
            database_name (str): Name of database.

        Returns:
            Database
        """
        return Database(self, database_name)

    def all_databases(self):
        """
        Provide all Databases on the server.

        GET /_all_dbs

        Returns:
            list (Database): All databases found, connected with this client.

        Raises:
            GatewayDown: When sync gateway instance can not be reached by
                client.
        """
        response = self.get('{}{}'.format(self.url, '_all_dbs')).json()
        return [self.get_database(name) for name in response]

    # --- REST Verbs ---

    @sg_method
    def get(self, url, **kwargs):
        return get(url, **kwargs)

    @sg_method
    def put(self, url, data):
        return put(url, json=data)

    @sg_method
    def delete(self, url, **kwargs):
        return delete(url, **kwargs)
