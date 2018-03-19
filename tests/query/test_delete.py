from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.exceptions import DoesNotExist


@pytest.fixture
def existing_query(query):
    """
    Returns:
        Query: Written to Sync Gateway with no views.
    """
    query.create_update()
    return query


def test_existing_query(existing_query):
    result = existing_query

    assert result.retrieve()


# --- TESTS ---


def test(existing_query):
    result = existing_query.delete()

    assert result is True
    with pytest.raises(DoesNotExist):
        existing_query.retrieve()


# --- FAILURES ---


def test_missing(query):
    with pytest.raises(DoesNotExist):
        query.delete()
