from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: Created in sync gateway.
    """
    database = Database(admin_client, 'test')
    database.create()
    return database
