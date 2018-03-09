from __future__ import absolute_import, print_function, unicode_literals

from .helpers import ComparableMixin


class AdminClient(object, ComparableMixin):
    """
    SyncGateway client for performing admin actions on the private admin port.
    This client is hardened to handle the Sync Gateway endpoint not being
    available - for example if Couchbase is being restarted.

    Attributes:
        url (str): URL of admin port.
    """

    def __init__(self, url):
        """
        Args:
            url (str): Pass base Sync Gateway URL (excluding database but
                including trailing slash) for this instance to connect to.
        """
        self.url = url

    def __repr__(self):
        return '<AdminClient on "{url}">'.format(url=self.url)

    def __lt__(self, other):
        """
        Two AdminClient instances are the same if they are both talking to the
        same URL (there is no username / password to distinguish them).

        Returns:
            bool

        Raises:
            AssertionError: When `other` is not an AdminClient.
        """
        assert isinstance(other, AdminClient)
        return self.url < other.url
