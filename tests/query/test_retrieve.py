from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Query
from pysyncgateway.exceptions import DoesNotExist


@pytest.fixture
def tiny_view(query):
    """
    Returns:
        Query: Called 'all_lists', written to Sync Gateway with a tiny map
            function.
    """
    query.data = {
        'views': {
            'tiny': {
                'map': '// Hello World',
            },
        },
    }
    query.create_update()
    return query


# --- TESTS ---


def test(tiny_view, database):
    query = Query(database, 'all_lists')

    result = query.retrieve()

    assert result is True
    assert '// Hello World' in query.data['views']['tiny']['map']


# --- FAILURES ---


def test_missing_query(query):
    with pytest.raises(DoesNotExist):
        query.retrieve()
