

import pytest

from pysyncgateway import Database, User


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: Created in sync gateway.
    """
    database = Database(admin_client, 'db')
    database.create()
    return database


@pytest.fixture
def user(database):
    """
    Returns:
        User: 'test-user' on Database 'db'. Not written to sync gateway.
    """
    return User(database, 'test-user')


@pytest.fixture
def existing_user(user):
    """
    Returns:
        User: User written to sync gateway with two channels.
    """
    user.set_password('__PASSWORD__')
    user.set_admin_channels('creator.test', 'approval.test.1234')
    user.create_update()
    return user
