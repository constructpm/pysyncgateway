from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: 'db' database written to Sync Gateway.
    """
    database = Database(admin_client, 'db')
    database.create()
    return database
