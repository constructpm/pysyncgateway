from __future__ import absolute_import, print_function, unicode_literals


class Stats(object):
    """
    Stats object from the expvars endpoint on the Sync Gateway. See
    https://github.com/couchbase/sync_gateway/wiki/expvars

    NOTE: Stats come from the server and not from the database.

    Attributes:
        client (AdminClient): Used to communicate with the server.
        data (dict): Statistical data populated after retrieval. Will be empty
            dictionary before retrieval.
        url (str): Location of stats.
    """

    def __init__(self, client):
        """
        Args:
            client (AdminClient): Used to communicate with the server.
        """
        self.client = client
        self.url = '{}_expvar'.format(self.client.url)
        self.data = {}

    def retrieve(self):
        """
        Load stats, parse info and stash in data attr.

        Returns:
            bool: load was successful.

        Raises:
            GatewayDown: When the endpoint can't be reached.
            ValueError: When something non-JSON is loaded.

        Side effects:
            data: Populated with dictionary parsed from the JSON response.
        """
        response = self.client.get(self.url)
        self.data = response.json()
        return True
