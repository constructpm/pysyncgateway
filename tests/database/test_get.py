from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database
from pysyncgateway.exceptions import DoesNotExist


def test(admin_client):
    database = Database(admin_client, 'db')
    database.create()

    result = database.get()

    assert result['db_name'] == 'db'


# --- FAILURES ---


def test_missing(admin_client):
    database = Database(admin_client, 'db')

    with pytest.raises(DoesNotExist):
        database.get()
