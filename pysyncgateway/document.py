from __future__ import absolute_import, print_function, unicode_literals


class Document(object):  # Resource):
    """
    A Couchbase Document in a database.

    Attributes:
        channels (tuple (str)): List of channels this document is in.
        data (DataDict): Data from the Document using the `DataDict` manager.
            The `DataDict` instance prevents protected keys from entering the
            data, but does nothing to prevent mutation. Therefore it never
            contains the private SG fields '_id', '_rev', 'channels'.
        doc_id (str): ID of document.
        rev (str): Revision identifier of document.
    """

    def __init__(self, database, doc_id):
        # super(Document, self).__init__(database)
        # assert_valid_document_id(doc_id)
        self.doc_id = doc_id
        self.rev = None
        self.channels = None
