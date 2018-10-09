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
        to_delete (bool): Flag used by :py:meth:`.Document.flatten_data()`.
            When set it generates data used to delete the Document when posted
            with :py:meth:`.Database.bulk_docs()`.
        open_revisions (list (Document)): List of previous revisions as
            Document instances. This will be populated when
            :py:meth:`.Document.retrieve()` is called with ``revs=True``.
        url (str): URL for this resource on Sync Gateway.
    """

    def __init__(self, database, doc_id):
        """
        Args:
            database (Database)
            doc_id (str)

        Raises:
            .InvalidDocumentID: When doc_id is not valid.
        """
        super(Document, self).__init__(database)
        assert_valid_document_id(doc_id)
        self.channels = ()
        self.doc_id = doc_id
        self.open_revisions = []
        self.rev = ''
        self.to_delete = False
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
            .InvalidChannelName: When a bad channel name is passed.
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

    def flatten_data(self):
        """
        Used when posting multiple documents with
        :py:meth:`.Database.bulk_docs()` to the ``/_bulk_docs`` endpoint. Set
        the ``to_delete`` flag on the Document instance if it should be
        deleted - only the particular revision will be marked for deletion, not
        all open revisions.

        Returns:
            dict: Data for this document including ``_rev`` and ``_id``.

        Raises:
            ValueError: Document needs a rev to be deletable.
        """
        if self.to_delete:
            data = {'_deleted': True}
        else:
            data = self.data.to_dict()
        data['_id'] = self.doc_id
        if self.rev:
            data['_rev'] = self.rev
        elif self.to_delete:
            raise ValueError('Document needs a rev to be deletable')
        return data

    def create_update(self):
        """
        Save or update Document in Sync Gateway. Saves the received revision id
        into instance's ``rev`` attribute.

        ``PUT /<database_name>/<doc_id>``

        Note:
            Works for updates but is not tested.

        Returns:
            int: ``AdminClient.CREATED`` if document was created (matches 201).

        Raises:
            .RevisionMismatch: When create (no revision) is tried on an
                existing Document or update is tried on an existing document,
                but the revision numbers do not match.  Two args are passed to
                the exception: url of the document and any revision that was
                passed with the ``PUT`` request.
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

        return False

    def _update_from_response(self, response_data):
        """
        Use response data from SG to update Document.
        """
        self.set_rev(response_data['_rev'])
        if 'channels' in response_data:
            self.set_channels(*response_data['channels'])

        self.data = response_data

    def retrieve(self):
        """
        Load document contents. Once loaded, ``_rev`` and ``channels`` are used
        to update the internal attributes before the data is sent to the
        DataDict.

        ``GET /<name>/<doc_id>``

        Returns:
            bool: Load was successful.

        Raises:
            .DoesNotExist: Document with provided doc_id can not be loaded.

        Note:
            DataDict never contains the private Sync Gateway fields ``_id``,
            ``_rev``, ``channels``.

        Note:
            **Not** running through ``/<name>/_raw/<doc_id>``.

        Warning:
            Side effect: ``self.channels`` is updated based on returned the
            JSON using ``self.set_channels()``.

        Warning:
            Side effect: ``self.data`` is updated with data dictionary loaded
            from JSON.

        Warning:
            Side effect: ``self.rev`` is updated from revision passed in JSON
            using ``self.set_rev``.
        """
        response = self.database.client.get(self.url)
        self._update_from_response(response.json())
        return True

    def get_open_revisions(self, include_deleted=False):
        """
        Retrieve all leaf revisions of this document and update this instance
        with the currently winning revision's data.

        Sync Gateway provides the leaf revision documents "as is" with no flag
        that one or other is the current document. Therefore this function
        makes two requests:

        * A GET request using :py:meth:`.Document.retrieve()`. This is used to
          find the currently winning revision.

        * A GET request with ``?open_revs=all`` to collect all leaf nodes.

        The list of leaf nodes is iterated and the currently winning revision
        is used to update this instance. Losing leaf revisions are blown up
        into :py:class:`.Document` instances and stored in the
        ``open_revisions`` list.

        Args:
            include_deleted (bool, Optional): When set to ``True``, Documents
                found that are not currently the winning revision and contain
                ``{'_deleted': True}`` are ignored. Defaults to ``False``.

        Returns:
            int: Number of open revisions found including the current revision.

        Raises:
            RevisionMismatch: When winning revision's rev was not found when
                the open revisions were loaded. This usually means that the
                winning revision was deleted before the open revisions could be
                retrieved. (untested and needs improvement to avoid race
                condition.)
        """
        self.open_revisions = []
        winning_check = self.database.client.get(self.url)
        winning_rev = winning_check.json()['_rev']

        response = self.database.client.get(
            self.url,
            params={'open_revs': 'all'},
            # When requesting open_revs, response switches to be multipart
            # format unless JSON is explicitly requested:
            # https://docs.couchbase.com/sync-gateway/1.5/admin-rest-api.html#/document/get__db___doc_
            headers={'Accept': 'application/json'},
        )

        found_winning = False
        count = 0
        for leaf in response.json():
            leaf_data = leaf['ok']
            if leaf_data['_rev'] == winning_rev:
                # Use winning revision to update this instance
                count += 1
                found_winning = True
                self._update_from_response(leaf_data)
            else:
                # Push open revisions into open_revisions list
                if leaf_data.get('_deleted') and not include_deleted:
                    continue
                count += 1
                open_rev = Document(self.database, self.doc_id)
                open_rev._update_from_response(leaf_data)
                self.open_revisions.append(open_rev)

        if not found_winning:
            raise RevisionMismatch('Revision "{}" not found in open revisions'.format(winning_rev))

        return count

    def delete(self):
        """
        Delete Document from its Database. Document must have been retrieved in
        order for a valid revision ID to be provided. If there isn't a cache of
        this information when a `delete` is asked for, then a pre-fetch will
        occur.

        Uses the default :py:meth:`.Client.delete()` action, but then inspects
        the response to ensure that ``{"ok": true}``.

        ``DELETE /<name>/<doc_id>?rev=<rev>``

        Returns:
            bool: Delete was successful.

        Raises:
            .DoesNotExist: If Document can't be found (doc has to be loaded
                first to retrieve the revision number, which can yield a 404 if
                it doesn't exist). Also can be raised if the Database does not
                exist.
            .RevisionMismatch: Provided ``rev`` parameter did not match the
                live revision ID on Sync Gateway at request time.
        """
        if not self.rev:
            self.retrieve()

        params = {
            'rev': self.rev,
        }

        response = self.database.client.delete(self.url, params=params)

        return response.status_code == 200 and response.json()['ok']
