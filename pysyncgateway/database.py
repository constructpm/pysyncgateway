from __future__ import absolute_import, print_function, unicode_literals

from .helpers import ComparableMixin, assert_valid_database_name


class Database(object, ComparableMixin):
    """
    A Couchbase Database.

    Attributes:
        client (AdminClient)
        name (str)
        url (str): URL to the database, created at init time, including
            trailing slash.
    """

    def __init__(self, client, name):
        """
        Args:
            client (AdminClient)
            name (str): A valid database name.
        """
        try:
            assert client.url > '', 'Please set a URL of something longer than empty string'
        except (AttributeError):
            message = (
                'Database needs a `client` that provides a populated `url` '
                'attribute (usually an `AdminClient` instance), '
                'not {}'
            ).format(type(client).__name__)
            raise ValueError(message)

        assert_valid_database_name(name)

        self.client = client
        self.name = name
        self.url = '{}{}/'.format(self.client.url, self.name)

    def __repr__(self):
        return '<Database "{url}">'.format(url=self.url)

    def __lt__(self, other):
        """
        Comparison is only carried out on the url, however this will call the
        current client's settings and use them to build the url each time.

        Args:
            other (Database)

        Returns:
            bool

        Raises:
            AssertionError: When other is not Database.
        """
        return self.url < other.url

    def create(self):
        """
        Write this Database instance to the server.

        Uses test orientated settings to create database, e.g. Walrus as
        server, since this function is intended for test functionality, rather
        than for API server to be regularly creating databases.

        PUT /:name/

        Returns:
            bool: Creation was successful.
        """
        data = {}
        response = self.client.put(self.url, data)
        return response.status_code == 201
