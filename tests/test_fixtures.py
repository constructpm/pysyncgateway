from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import AdminClient

from .conftest import admin_client as admin_client_fn


def test_admin_client_existing_database(admin_client, syncgateway_admin_url):
    database = admin_client.get_database('test')
    database.create()

    with pytest.raises(AssertionError) as excinfo:
        next(admin_client_fn(syncgateway_admin_url, False))

    assert '1 unexpected Databases [{}]'.format(database) in excinfo.value.args[0]


def test_admin_client_cleanup(syncgateway_admin_url):
    admin_client = AdminClient(syncgateway_admin_url)
    database = admin_client.get_database('test')
    database.create()
    admin_fixture = admin_client_fn(syncgateway_admin_url, True)
    next(admin_fixture)

    with pytest.raises(StopIteration):
        next(admin_fixture)

    assert admin_client.all_databases() == []
