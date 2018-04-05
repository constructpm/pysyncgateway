from __future__ import absolute_import, print_function, unicode_literals

from .document import Document
from .exceptions import DoesNotExist
from .helpers import ComparableMixin, assert_valid_database_name
from .query import Query
from .session import Session
from .user import User


class Database(ComparableMixin, object):
    """
    A Database on Sync Gateway.

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
        if not getattr(client, 'url', None):
            raise ValueError(
                '{class_name} needs a `client` that provides a populated '
                '`url` (usually a `AdminClient` instance), not {found}'.format(
                    class_name=self.__class__.__name__,
                    found=type(client).__name__,
                ),
            )

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
            ValueError: When other is not Database.
        """
        if not isinstance(other, Database):
            raise ValueError('Database compared to {}'.format(type(other)))
        return self.url < other.url

    def create(self):
        """
        Write this Database instance to Sync Gateway.

        Uses test orientated settings (i.e. none - the empty dictionary ``{}``
        is passed as data) to create database. This function is intended for
        test functionality, rather than for clients to be regularly creating
        databases.

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

        Raises:
            DoesNotExist: When database is not written to Sync Gateway
                regardless of whether the client is authorized or not.
            ClientUnauthorized: When database exists and client is not
                authorized.
        """
        response = self.client.get(self.url)
        return response.json()

    def delete(self):
        """
        Remove database.

        Whereas Sync Gateway will raise 404 if the database is not found, this
        fails silently with the intention that it can be used 'scatter gun'
        style at the end of test runs to clean up database lists.

        ``DELETE /:name/``

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
        """
        Returns:
            Document: An instance of Document in this Database with provided
            ``doc_id``.
        """
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
            by the endpoint. For each instance the ``data['_rev']`` value is
            populated with the revision ID from ``value.rev``.

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
            User: An instance of User for the provided ``username``.
        """
        return User(self, username)

    def all_users(self):
        """
        ``GET /:name/_user/``

        Returns:
            list (User): All Users in Database.
        """
        url = '{}_user/'.format(self.url)
        response = self.client.get(url)
        return [self.get_user(username) for username in response.json()]

    # --- Queries ---

    def get_query(self, doc_id):
        """
        Returns:
            Query: An instance of a query design document in this Database with
            the provided ``doc_id``.
        """
        return Query(self, doc_id)

    # --- Session ---

    def get_session(self):
        """
        Returns:
            Session
        """
        return Session(self)
