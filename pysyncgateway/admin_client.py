from __future__ import absolute_import, print_function, unicode_literals

from .client import Client


class AdminClient(Client):
    """
    Sync Gateway admin client for performing actions on the private admin API.

    Attributes:
        url (str): Sync Gateway admin REST API URL.
    """

    def __repr__(self):
        return '<AdminClient on "{url}">'.format(url=self.url)

    def __lt__(self, other):
        """
        Two AdminClient instances are the same if they are both talking to the
        same URL (there is no username / password to distinguish them).

        Returns:
            bool

        Raises:
            ValueError: When `other` is not an AdminClient.
        """
        if not isinstance(other, AdminClient):
            raise ValueError('AdminClient compared to {}'.format(type(other)))
        return self.url < other.url

    # --- Databases ---

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
