from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: 'db' database not created on sync gateway.
    """
    return Database(admin_client, 'db')
