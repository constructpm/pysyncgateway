from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database, Query


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: 'db' database written to Sync Gateway.
    """
    database = Database(admin_client, 'db')
    database.create()
    return database


@pytest.fixture
def query(database):
    """
    Returns:
        Query: Not written to Sync Gateway.
    """
    return Query(database, 'all_lists')
