from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.exceptions import DoesNotExist


def test_no_docs(database):
    database.create()

    result = database.bulk_docs([])

    assert result is True
    assert database.all_docs() == []


def test_new_docs(database):
    """
    Example taken from https://docs.couchbase.com/sync-gateway/1.5/resolving-conflicts.html
    """
    database.create()
    doc = database.get_document('foo')
    doc.data = {
        'type': 'user',
        'updated_at': '2016-06-24T17:37:49.715Z',
        'status': 'online',
    }
    doc.set_rev('1-123')

    result = database.bulk_docs([doc])

    assert result is True
    assert database.all_docs() == [doc]


def test_new_docs_conflicted(database):
    """
    Example taken from https://docs.couchbase.com/sync-gateway/1.5/resolving-conflicts.html
    """
    database.create()
    doc_123 = database.get_document('foo')
    doc_123.data = {
        'type': 'user',
        'updated_at': '2016-06-24T17:37:49.715Z',
        'status': 'online',
    }
    doc_123.set_rev('1-123')
    doc_456 = database.get_document('foo')
    doc_456.data = {
        'type': 'user',
        'updated_at': '2016-06-26T17:37:49.715Z',
        'status': 'offline',
    }
    doc_456.set_rev('1-456')
    doc_789 = database.get_document('foo')
    doc_789.data = {
        'type': 'user',
        'updated_at': '2016-06-25T17:37:49.715Z',
        'status': 'offline',
    }
    doc_789.set_rev('1-789')

    result = database.bulk_docs([doc_123, doc_456, doc_789])

    assert result is True
    assert database.all_docs() == [doc_123]


# --- FAILURES ---


def test_missing_database(database):
    with pytest.raises(DoesNotExist):
        database.bulk_docs([])
