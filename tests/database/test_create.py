from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Database


def test(admin_client):
    database = Database(admin_client, 'test_newnewdb')

    result = database.create()

    assert result is True
    assert database in admin_client.all_databases()


# --- FAILURES ---


def test_collision(admin_client):
    """
    Database can't be created if already exists
    """
    existing_database = admin_client.get_database('test_collision')
    existing_database.create()

    result = admin_client.get_database('test_collision').create()

    assert result is False
