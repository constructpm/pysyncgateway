from __future__ import absolute_import, print_function, unicode_literals


def test_database(database, admin_client):
    result = database

    assert result in admin_client.all_databases()
