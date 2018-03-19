from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Query
from pysyncgateway.exceptions import DoesNotExist


@pytest.fixture()
def database_with_doc(database):
    """
    Returns:
        Database: Database with a single document called 'stuff' written to
            Sync Gateway.
    """
    database.get_document('stuff').create_update()
    return database


@pytest.fixture
def all_query(database_with_doc):
    """
    Returns:
        Query: Called 'all' and containing a single view called 'everything' to
            retrieve all documents (just like 'all_docs' but manual), written
            to Sync Gateway.
    """
    query = Query(database_with_doc, 'all')
    query.data = {
        'views': {
            'everything': {
                'map': 'function(doc,meta){emit(meta.id,doc);}',
            },
        },
    }
    query.create_update()
    return query


# --- TESTS ---


def test_default(all_query):
    result = all_query.query_view('everything')

    assert result['total_rows'] == 1
    assert result['rows'][0]['key'] == 'stuff'


def test_default_stale(all_query, database_with_doc):
    """
    Hot-up the view, add an additional document and only the first doc comes
    back in query.
    """
    all_query.query_view('everything')
    database_with_doc.get_document('moarstuff').create_update()

    result = all_query.query_view('everything')

    assert result['total_rows'] == 1
    assert result['rows'][0]['key'] == 'stuff'


def test_unstale(all_query, database_with_doc):
    """
    Hot view updates itself when `stale=False` is passed.
    """
    all_query.query_view('everything')
    database_with_doc.get_document('moarstuff').create_update()

    result = all_query.query_view('everything', stale=False)
    result = all_query.query_view('everything', stale=False)
    result = all_query.query_view('everything', stale=False)
    result = all_query.query_view('everything', stale=False)

    assert result['total_rows'] == 2
    assert sorted([r['key'] for r in result['rows']]) == ['stuff', 'moarstuff']

# --- FAILURES ---


def test_missing(query):
    with pytest.raises(DoesNotExist):
        query.query_view('stuff')
