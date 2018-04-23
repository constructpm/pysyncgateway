from __future__ import absolute_import, print_function, unicode_literals

import json

from .resource import Resource


class Query(Resource):
    """
    Query a design document.

    Attributes:
        data (DataDict): Data from the design document using the ``DataDict``
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

        ``PUT /<database_name>/_design/<doc_id>``

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

    def query_view(self, view_name, key=None, stale=True, timeout=None):
        """
        Load a view function from this design Document. Document must be
        written to Sync Gateway and view's Javascript function must be valid.

        Args:
            view_name (str): View's name.
            key (Optional): Value to use to search the view's key (the
                left part of the map). Any type can be passed as long as:

                * ``key is not None``

                * ``key`` can be serialized to a string by ``json.dumps()``.

                To query a view with multiple keys set ``key`` as an iterable
                which will be serialized to JSON as an array. E.g.
                ``key=['left_id', 'right_id']``.
            stale (bool, Optional): Allow stale results in the view. This is
                currently the default value in Sync Gateway, so is only passed
                when set to ``False``. Default ``True``.

                ``'false'`` is an undocumented option for this param. See
                https://github.com/couchbase/sync_gateway/issues/727#issuecomment-83588984

                It also doesn't work in Walrus mode, see
                https://github.com/constructpm/pysyncgateway/issues/7
            timeout (int, Optional): Set a time out of seconds as per requests'
                spec which means that if the Sync Gateway does not respond to
                the GET request within the ``timeout`` period, a ``ReadTimeout``
                will be raised.  Default ``None`` which means that requests'
                default is used.

        Returns:
            dict: Decoded JSON for view data result. Will usually be a
            dictionary contain keys 'Collator', 'rows' and 'total_rows'.

        Raises:
            DoesNotExist: When database, design document or contained view can
                not be found.
            requests.exceptions.ReadTimeout: When Sync Gateway does not respond
                within given ``timeout``.
        """
        # Build params (passed to SG in the URL)
        params = {}
        if not stale:
            params['stale'] = 'false'
        if key is not None:
            params['key'] = json.dumps(key)

        # Build kwargs (passed to requests.get)
        kwargs = {}
        if params:
            kwargs['params'] = params
        if timeout is not None:
            kwargs['timeout'] = timeout

        url = self.build_view_url(view_name)
        response = self.database.client.get(url, **kwargs)

        return response.json()
