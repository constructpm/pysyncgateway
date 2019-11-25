

import pytest


@pytest.fixture
def database_with_docs(database):
    """
    Returns:
        Database: Database containing two documents about Homer and Marge.
    """
    database.create()
    doc_homer = database.get_document('homer')
    doc_homer.data = {'food': 'donuts'}
    doc_homer.create_update()
    doc_marge = database.get_document('marge')
    doc_marge.data = {'hair': 'blue'}
    doc_marge.create_update()
    return database


def test_database_with_docs(database_with_docs):
    result = database_with_docs

    assert len(result.all_docs()) == 2


# --- TESTS ---


def test(database, admin_client):
    database.create()

    result = database.delete()

    assert result is True
    assert database not in admin_client.all_databases()


def test_delete_resurrect_database(database):
    """
    Database recreation does not bring back documents. This is a legacy issue
    with SG ~v1.3 in Walrus mode where deleting a database would not purge the
    documents in it. Kept for test sanity.
    """
    database.delete()
    database.create()

    result = database.all_docs()

    assert result == []


# --- FAILURES ---


def test_does_not_exist(database):
    result = database.delete()

    assert result is False
