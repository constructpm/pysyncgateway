from __future__ import absolute_import, print_function, unicode_literals

from .document import Document
from .exceptions import DoesNotExist
from .helpers import ComparableMixin, assert_valid_database_name
from .user import User


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
        assert isinstance(other, Database)
        return self.url < other.url

    def create(self):
        """
        Write this Database instance to the server.

        Uses test orientated settings to create database, e.g. Walrus as
        server, since this function is intended for test functionality, rather
        than for API server to be regularly creating databases.

        ``PUT /:name/``

        Returns:
            bool: Creation was successful.
        """
        return self.client.put(self.url, {}).status_code == 201

    def get(self):
        """
        Return information about this Database from Sync Gateway.

        ``GET /:name/``

        Returns:
            dict: Information loaded from SG.
        """
        response = self.client.get(self.url)
        return response.json()

    def delete(self):
        """
        Remove database.

        Whereas SyncGateway will raise 404 if the database is not found, this
        fails silently with the intention that it can be used 'scatter gun'
        style at the end of test runs to clean up database lists. Since
        documents appear to hang around after database delete, this gets a list
        of all document IDs in the database and removes them before dropping
        the DB.

        ``DELETE /:name/``

        NOTE this code is not optimal and there may be some value in using a
        _purge call instead / as well. This from Simon @ couchbase:

            I've just confirmed that you need to delete, then purge the
            documents.

        Returns:
            bool: Database was found and deleted.
        """
        try:
            response = self.client.delete(self.url)
        except DoesNotExist:
            return False
        return response.status_code == 200

    # --- Documents ---

    def get_document(self, doc_id):
        return Document(self, doc_id)

    def all_docs(self):
        """
        Get list of all Documents in database.

        ``GET /:name/_all_docs``

        NOTE Use for testing only. From Simon @ Couchbase:

            We would strongly advise against using the `_all_docs` endpoint. As
            your database grows relying on the View that this calls to return
            to you every document key is inadvisable and does not scale well to
            very high numbers of documents.

            If you need to retrieve or update multiple documents please use the
            _bulk_get and _bulk_docs end points to supply a list of keys (or
            documents) for retrieval or update.

        Returns:
            list (Document): An instance of Document for each document returned
                by the endpoint. For each instance the `data['_rev']` value is
                populated with the revision ID from `value.rev`.

        Raises:
            DoesNotExist: Database can't be found on sync gateway.
        """
        url = '{}{}'.format(self.url, '_all_docs')

        response = self.client.get(url)

        documents = []

        for doc_info in response.json()['rows']:
            document = self.get_document(doc_info['id'])
            document.set_rev(doc_info['value']['rev'])
            documents.append(document)

        return documents

    # --- Users ---

    def get_user(self, username):
        """
        Returns:
            User: An instance of ``User`` for the provided ``username``.
        """
        return User(self, username)

    def all_users(self):
        """
        ``GET /:name/_user/`` (undocumented endpoint)

        Returns:
            list (User): All Users in Database.
        """
        url = '{}_user/'.format(self.url)
        response = self.client.get(url)
        return [self.get_user(username) for username in response.json()]
