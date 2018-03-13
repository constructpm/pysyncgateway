from __future__ import absolute_import, print_function, unicode_literals

from .exceptions import RevisionMismatch
from .helpers import assert_valid_channel_name, assert_valid_document_id
from .resource import Resource


class Document(Resource):
    """
    A Couchbase Document in a database.

    Attributes:
        channels (tuple (str)): Channels this document is in.
        data (DataDict): Data from the Document using the `DataDict` manager.
            The `DataDict` instance prevents protected keys from entering the
            data, but does nothing to prevent mutation. Therefore it never
            contains the private SG fields '_id', '_rev', 'channels'.
        doc_id (str): ID of document.
        rev (str): Revision identifier of document. Set to empty string when no
            document has been retrieved.
        url (str): URL for this resource on sync gateway.
    """

    def __init__(self, database, doc_id):
        """
        Args:
            database (Database)
            doc_id (str)

        Raises:
            InvalidDocumentID: When doc_id is not valid.
        """
        super(Document, self).__init__(database)
        assert_valid_document_id(doc_id)
        self.doc_id = doc_id
        self.rev = ''
        self.channels = ()
        self.url = '{}{}'.format(self.database.url, self.doc_id)

    def set_channels(self, *channels):
        """
        Validate each channel passed and save to channels attribute. No update
        to channels is made if one is bad, all are rejected.

        Args:
            *args (str): Channels to be set for this document.

        Returns:
            None

        Raises:
            InvalidChannelName: When a bad channel name is passed.
        """
        for channel in channels:
            assert_valid_channel_name(channel)
        self.channels = channels

    def set_rev(self, revision_id):
        """
        Set Document's revision id. This is used for subsequent updates and
        deletions. Not checked for any validity.

        Args:
            revision_id (str)

        Returns:
            None

        Raises:
            ValueError: When revision_id is empty string.
        """
        if not revision_id:
            raise ValueError('Empty revision received')
        self.rev = revision_id

    def create_update(self):
        """
        Save or update Document in sync gateway. Saves the received revision id
        into Documents `rev` attribute.

        PUT /<database_name>/<doc_id>
        Response has keys: ('id', 'rev', 'ok')

        NOTE: works for updates but is not tested.

        Returns:
            int: AdminClient.CREATED if document was created (matches 201).
        """

        put_data = self.data.to_dict()

        if self.channels is not None:
            put_data['channels'] = self.channels
        if self.rev is not None:
            put_data['_rev'] = self.rev

        response = self.database.client.put(self.url, data=put_data)

        if response.status_code == 201:
            response_data = response.json()
            self.set_rev(response_data['rev'])
            return self.database.client.CREATED
        elif response.status_code == 409:
            raise RevisionMismatch(response.json())

        return False
