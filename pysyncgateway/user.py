from __future__ import absolute_import, print_function, unicode_literals

import six

from .exceptions import DoesNotExist, InvalidPassword
from .helpers import assert_valid_channel_name
from .resource import Resource


class User(Resource):
    """
    A User in a Database.

    Attributes:
        admin_channels (tuple(str)): Channels that this User has been added to
            by admin or sync function.
        data (DataDict)
        name (str): Username of this user.
        password (str): User's password. Can be `None` and is only set with
            `set_password`.
        retrieved (bool): User been retrieved from sync gateway. Acts as a flag
            to know if there should be a password sent at `create_update` time.
        url (str): URL for this User on sync gateway.
    """

    def __init__(self, database, name):
        """
        Args:
            database (Database)
            name (str): User name.
        """
        super(User, self).__init__(database)
        self.admin_channels = ()
        self.name = name
        self.password = None
        self.retrieved = False
        self.url = '{}_user/{}'.format(self.database.url, self.name)

    def set_password(self, password):
        """
        Args:
            password (str): A password for the User. Must not be empty (this is
                a basic security measure and is not enforced by sync gateway.

        Raises:
            InvalidPassword: Password provided for User was invalid.
        """
        if not password or not isinstance(password, six.string_types):
            raise InvalidPassword('"{}" is not a valid password for a User'.format(password))
        self.password = password

    def set_admin_channels(self, *channels):
        """
        Validate each channel passed in `channels` and save to `admin_channels`
        attribute. No update to channels is made if one is bad, all are
        rejected.

        Args:
            *args: Variable number of channels as str.

        Raises:
            InvalidChannelName: Bad channel name is received.
        """
        for channel in channels:
            assert_valid_channel_name(channel)
        self.admin_channels = channels

    def create_update(self):
        """
        Create a new or update an existing user for currently connected
        database. When creating a new User then their password must have been
        set on this instance using `set_password`, or the sync gateway will
        reject the PUT with a 400.

        NOTE it's not possible to change the username (name) of a user with
        this function.

        NOTE Does not handle roles, email or disabled state.

        `PUT /<database_name>/_user/<name>`

        Returns:
            int: `AdminClient.CREATED` if a new user was created (matches 201),
                `AdminClient.UPDATED` if an existing user was updated,

        Raises:
            DoesNotExist: When Database does not exist.
            SyncGatewayClientErrorResponse: When sync gateway returns a client
                error HTTP code.
        """
        data = {
            'admin_channels': self.admin_channels,
            'name': self.name,
        }

        if not self.retrieved:
            data['password'] = self.password

        response = self.database.client.put(self.url, data)

        if response.status_code == 201:
            return self.database.client.CREATED
        elif response.status_code == 200:
            return self.database.client.UPDATED

        # If code reaches here, there's an unexpected HTTP status code.

    def retrieve(self):
        """
        Get User's info from sync gateway.

        When User is found the response's payload is kept in the `data`
        attribute.

        When User is not found (404), any existing `data` is erased.
        Sync gateway response can optionally contain an `admin_channels` field.
        When none are returned then `admin_channels` attribute of the User is
        set to the empty tuple.

        `GET /<database_name>/_user/<name>`

        Returns:
            bool: Retrieval was successful.

        Raises:
            DoesNotExist: User can't be found in this Database or Database does
                not exist.
        """
        try:
            response = self.database.client.get(self.url)
        except DoesNotExist:
            self.data = {}
            raise

        self.data = response.json()
        self.retrieved = True

        try:
            self.set_admin_channels(*self.data['admin_channels'])
        except KeyError:
            self.set_admin_channels()

        return True

    def delete(self):
        """
        Delete User from Database.

        Returns:
            bool: User was deleted.

        Raises:
            DoesNotExist: User can't be found in this Database or Database does
                not exist.
        """
        response = self.database.client.delete(self.url)
        result = response.status_code == 200
        if result:
            self.retrieved = False
        return result
