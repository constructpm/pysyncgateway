from __future__ import absolute_import, print_function, unicode_literals


def test_empty(admin_client):
    result = admin_client.all_databases()

    assert result == []
