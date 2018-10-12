from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.exceptions import DoesNotExist


def test_simple(recipe_document):
    result = recipe_document.get_open_revisions()

    assert result == 1
    assert recipe_document.open_revisions == []


def test_revisions(conflicted_document):
    """
    conflicted_document starts at rev 1-123, but it is updated to the current
    winning revision.
    """
    result = conflicted_document.get_open_revisions()

    assert result == 3
    assert conflicted_document.rev == '1-789'
    assert conflicted_document.data == {
        'type': 'user',
        'updated_at': '2016-06-25T17:37:49.715Z',
        'status': 'offline',
    }
    assert len(conflicted_document.open_revisions) == 2
    assert conflicted_document.open_revisions[0] == conflicted_document
    assert conflicted_document.open_revisions[1] == conflicted_document
    assert sorted([doc.rev for doc in conflicted_document.open_revisions]) == [
        '1-123',
        '1-456',
    ]


def test_revisions_ignores_deleted(conflicted_document, database):
    """
    Remove open rev at position 0 and this leaves the other open rev which was
    the one at position 1. Note: The open revisions are returned in a
    non-deterministic way.
    """
    conflicted_document.get_open_revisions()
    conflicted_document.open_revisions[0].to_delete = True
    expected_remaining_rev = conflicted_document.open_revisions[1].rev
    database.bulk_docs(conflicted_document.open_revisions[:1], new_edits=None)

    result = conflicted_document.get_open_revisions()

    assert result == 2
    assert [doc.rev for doc in conflicted_document.open_revisions] == [expected_remaining_rev]


def test_revisions_include_deleted(conflicted_document, database):
    conflicted_document.get_open_revisions()
    conflicted_document.open_revisions[0].to_delete = True
    conflicted_document.open_revisions[1].to_delete = True
    database.bulk_docs(conflicted_document.open_revisions, new_edits=None)

    result = conflicted_document.get_open_revisions(include_deleted=True)

    assert result == 3
    assert [doc.data for doc in conflicted_document.open_revisions] == [
        {
            '_deleted': True
        },
        {
            '_deleted': True
        },
    ]


def test_reload(conflicted_document):
    conflicted_document.get_open_revisions()

    result = conflicted_document.get_open_revisions()

    assert result == 3
    assert conflicted_document.rev == '1-789'
    assert conflicted_document.data == {
        'type': 'user',
        'updated_at': '2016-06-25T17:37:49.715Z',
        'status': 'offline',
    }
    assert len(conflicted_document.open_revisions) == 2


# --- FAILURES ---


def test_missing(empty_document):
    with pytest.raises(DoesNotExist):
        empty_document.get_open_revisions()
