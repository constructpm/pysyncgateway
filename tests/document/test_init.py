from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Document


def test(database):
    result = Document(database, '__DOC_ID__')

    assert result.doc_id == '__DOC_ID__'
    assert result.rev == ''
    assert result.channels == ()
