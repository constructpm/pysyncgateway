from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import Database, UserClient
from pysyncgateway.exceptions import ClientUnauthorized, DoesNotExist


@pytest.fixture
def existing_database(database):
    """
    Returns:
        Database: Created in sync gateway.
    """
    database.create()
    return database


@pytest.fixture
def user_client(syncgateway_public_url):
    """
    Returns:
        UserClient: Unauthorized client.
    """
    return UserClient(syncgateway_public_url)


# --- TESTS ---


def test(existing_database):
    result = existing_database.get()

    assert result['db_name'] == 'db'


def test_user_authed(existing_database, user_client):
    user = existing_database.get_user('user')
    user.set_password('__PASSWORD__')
    user.create_update()
    user_client.auth('user', '__PASSWORD__')
    user_database = user_client.get_database('db')

    result = user_database.get()

    assert result['db_name'] == 'db'


# --- FAILURES ---


def test_missing(admin_client):
    database = Database(admin_client, 'db')

    with pytest.raises(DoesNotExist):
        database.get()


def test_user_unauthed(existing_database, user_client):
    user_database = user_client.get_database('db')

    with pytest.raises(ClientUnauthorized) as excinfo:
        user_database.get()

    assert 'Login required' in excinfo.value.message
