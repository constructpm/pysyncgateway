

import pytest


def test_empty(empty_document):
    result = empty_document.flatten_data()

    assert result == {
        '_id': 'empty_document',
    }


def test_empty_with_rev(empty_document):
    empty_document.set_rev('9-00aabbccddeeff')

    result = empty_document.flatten_data()

    assert result == {
        '_id': 'empty_document',
        '_rev': '9-00aabbccddeeff',
    }


def test_some_data_and_rev(database):
    document = database.get_document('user.999|requirements')
    document.data = {
        'updated_at': '2016-06-26T17:37:49.715Z',
        'status': 'offline',
    }
    document.set_rev('101-745062ff812078461f4cc3f7f7b330cf')

    result = document.flatten_data()

    assert result == {
        '_id': 'user.999|requirements',
        '_rev': '101-745062ff812078461f4cc3f7f7b330cf',
        'updated_at': '2016-06-26T17:37:49.715Z',
        'status': 'offline',
    }


def test_some_data_and_rev_to_delete(database):
    document = database.get_document('user.999|requirements')
    document.data = {
        'updated_at': '2016-06-26T17:37:49.715Z',
        'status': 'offline',
    }
    document.set_rev('101-745062ff812078461f4cc3f7f7b330cf')
    document.to_delete = True

    result = document.flatten_data()

    assert result == {
        '_id': 'user.999|requirements',
        '_rev': '101-745062ff812078461f4cc3f7f7b330cf',
        '_deleted': True,
    }


# --- FAILURES ---


def test_empty_delete(empty_document):
    empty_document.to_delete = True

    with pytest.raises(ValueError) as excinfo:
        empty_document.flatten_data()

    assert 'needs a rev' in str(excinfo)
