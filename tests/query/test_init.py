from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Query


def test(database):
    result = Query(database, '__DESIGN_DOC_ID__')

    assert result.doc_id == '__DESIGN_DOC_ID__'
    assert result.url == 'http://localhost:4985/db/_design/__DESIGN_DOC_ID__'
