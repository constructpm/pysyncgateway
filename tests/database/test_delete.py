from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Database


def test_exists(admin_client):
    database = Database(admin_client, 'test')
    database.create()

    result = database.delete()

    assert result is True
    assert database not in admin_client.all_databases()


def test_does_not_exist(admin_client):
    database = Database(admin_client, 'test')

    result = database.delete()

    assert result is False


# TODO build out doc cleanup tests
