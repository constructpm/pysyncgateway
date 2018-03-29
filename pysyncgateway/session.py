from __future__ import absolute_import, print_function, unicode_literals

from .exceptions import NotLoaded
from .resource import Resource


class Session(Resource):
    """
    Sessions on the Database are undocumented as of Sync Gateway 1.5 in both
    the `public
    <https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/rest-api/index.html#/>`_
    and `admin
    <https://developer.couchbase.com/documentation/mobile/1.5/references/sync-gateway/admin-rest-api/index.html>`_
    REST APIs. But since they provide a useful test mechanism by showing a list
    of channels that the authenticated User has been subscribed to, they are
    included in this library.

    Attributes:
        data (DataDict): Data from the session using the ``DataDict`` manager.
        database (Database)
        url (str): URL for the session in the Database on Sync Gateway.
    """

    def __init__(self, database):
        """
        Args:
            database (Database)
        """
        super(Session, self).__init__(database)
        self.url = '{}_session'.format(self.database.url)

    def retrieve(self):
        """
        Collect session information for the current client in the ``database``
        attribute.

        For unauthorized users on the public API and requests on the admin API
        this looks like::

            {
                'authentication_handlers': ['default', 'cookie'],
                'ok': True,
                'userCtx': {
                    'channels': {},
                    'name': None,
                },
            }

        For authenticated users on the public API, in this example with the
        name ``__USERNAME__`` and channels ``a``, ``b`` and ``c``, this looks
        like::

            {
                'authentication_handlers': ['default', 'cookie'],
                'ok': True,
                'userCtx': {
                    'channels': {
                        '!': 1,
                        'a': 1,
                        'b': 1,
                        'c': 1,
                    },
                    'name': '__USERNAME__',
                },
            }

        Returns:
            bool: Success

        Raises:
            DoesNotExist: When database does not exist on Sync Gateway,
                regardless of whether client is authorized or not.

        Warning:
            Side effect: Updates ``self.data`` with response from Sync Gateway
            on success.
        """
        response = self.database.client.get(self.url)
        response_data = response.json()
        self.data = response_data
        return True

    def _get_user_ctx(self):
        try:
            return self.data['userCtx']
        except KeyError:
            raise NotLoaded()

    def get_name(self):
        """
        Helper to pick user's ``name`` field from retrieved session data.

        Returns:
            str: Name of user according to Sync Gateway.

        Raises:
            NotLoaded: When session has not been retrieved.
            KeyError: When the ``userCtx`` data in the session response does
                not contain a ``name`` field.
        """
        return self._get_user_ctx()['name']

    def get_channels(self):
        """
        Helper to pick user's subscribed channels from retrieved session data.

        Returns:
            list: Sorted list of channel names found in response including the
            special ``!`` public channel.

        Raises:
            NotLoaded: When session has not been retrieved.
            KeyError: When the ``userCtx`` data in the session response does
                not contain a ``channels`` dictionary.
        """
        return sorted(list(self._get_user_ctx()['channels']))
