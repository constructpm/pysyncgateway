from __future__ import absolute_import, print_function, unicode_literals

import pytest

from .conftest import admin_client as admin_client_fn


def test_admin_client_existing_database(admin_client, syncgateway_admin_url):
    database = admin_client.get_database('test')
    database.create()

    with pytest.raises(AssertionError) as excinfo:
        admin_client_fn(syncgateway_admin_url, False).next()

    assert '1 unexpected Databases [{}]'.format(database) in excinfo.value.message
