from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Document


def test(database):
    result = database.get_document('test')

    assert isinstance(result, Document)
    assert result.database == database
    assert result.doc_id == 'test'
