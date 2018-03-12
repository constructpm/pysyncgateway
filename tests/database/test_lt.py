from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Database


def test_equal(admin_client):
    database = Database(admin_client, 'test')

    result = database == Database(admin_client, 'test')

    assert result is True
