from __future__ import absolute_import, print_function, unicode_literals

from .resource import Resource


class Query(Resource):
    """
    Query a design document.

    Attributes:
        data (DataDict): Data from the design document using the `DataDict`
            manager.
        doc_id (str): ID of design document.
        url (str): URL for this resource on Sync Gateway.
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

    def create_update(self):
        """
        Create or update design document with data.

        `PUT /<database_name>/_design/<doc_id>`

        Returns:
            bool: Design document was created or updated successfully.
        """
        return self.database.client.put(self.url, data=self.data).status_code == 201

    def retrieve(self):
        """
        Returns:
            bool: Design document was retrieved.

        Raises:
            DoesNotExist: Design document or Database can not be found.

        Side effects:
            data: Updates internal data dictionary with data loaded from JSON.
        """
        response = self.database.client.get(self.url)
        self.data = response.json()
        return True

    def delete(self):
        """
        Delete design document.

        Returns:
            bool: Design document deleted.

        Raises:
            DoesNotExist: Design document or Database can not be found.
        """
        return self.database.client.delete(self.url).status_code == 200
