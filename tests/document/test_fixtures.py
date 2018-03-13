from __future__ import absolute_import, print_function, unicode_literals


def test_database(database, admin_client):
    result = database

    assert result in admin_client.all_databases()


def test_empty_document(empty_document):
    result = empty_document

    assert result.data == {}
    assert result.rev == ''
