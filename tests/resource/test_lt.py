from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database
from pysyncgateway.resource import Resource


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: test database not on sync gateway.
    """
    return Database(admin_client, 'test')


def test_eq(database):
    a_resource = Resource(database)
    a_resource.url = '__SOME_URL__'
    b_resource = Resource(database)
    b_resource.url = '__SOME_URL__'

    result = a_resource == b_resource

    assert result is True


def test_ne(database):
    a_resource = Resource(database)
    a_resource.url = '__SOME_URL__'
    b_resource = Resource(database)
    b_resource.url = '__OTHER_URL__'

    result = a_resource == b_resource

    assert result is False
