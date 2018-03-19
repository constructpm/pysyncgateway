from __future__ import absolute_import, print_function, unicode_literals

from .resource import Resource


class Query(Resource):
    """
    Query a design document.

    Attributes:
        doc_id (str): ID of design document.
        url (str): URL for this resource on sync gateway.
    """

    def __init__(self, database, doc_id):
        """
        Args:
            database (Database)
            doc_id (str): Design document name.
        """
        super(Query, self).__init__(database)
        self.doc_id = doc_id
        self.url = '{}_design/{}'.format(self.database.url, self.doc_id)

    def build_view_url(self, view_name):
        """
        Args:
            view_name (str)

        Returns:
            str: URL for querying view.
        """
        return '{}/_view/{}'.format(self.url, view_name)
