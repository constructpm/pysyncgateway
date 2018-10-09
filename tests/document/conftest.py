from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database, Document


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: Created in sync gateway.
    """
    database = Database(admin_client, 'test')
    database.create()
    return database


@pytest.fixture
def empty_document(database):
    """
    Returns:
        Document: Empty document not written to sync gateway.
    """
    return Document(database, 'empty_document')


@pytest.fixture
def recipe_document(database):
    """
    Returns:
        Document: Contains a recipe and written to sync gateway.
    """
    data = {
        'ingredients': ['chicken', 'butter'],
        'recipe': 'Mix the chicken and the butter. Voila!',
    }
    document = database.get_document('butter_chicken')
    document.data = data
    document.create_update()
    return document


@pytest.fixture
def permissions_document(database):
    """
    Returns:
        Document: Written to SG with empty data, just channels set.
    """
    document = database.get_document('permission-list')
    document.set_channels('acc.1234', 'acc.7882')
    document.create_update()
    return document


@pytest.fixture
def conflicted_document(database):
    """
    Returns:
        Document: Document 'foo' with 3 revisions. Returns the original
        revision '1-123', but instance is not retrieved.
    """
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
    database.bulk_docs([doc_123, doc_456, doc_789])
    return doc_123
