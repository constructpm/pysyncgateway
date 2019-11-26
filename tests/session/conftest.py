import pytest
from pysyncgateway import Database, UserClient


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
def session(database, syncgateway_public_url):
    """
    Returns:
        Session: With authenticated user '__USERNAME__' written to Sync
        Gateway.
    """
    user_client = UserClient(syncgateway_public_url)
    session = user_client.get_database('db').get_session()
    user = database.get_user('__USERNAME__')
    user.set_password('__PASSWORD__')
    user.set_admin_channels('a', 'b', 'c')
    user.create_update()
    user_client.auth('__USERNAME__', '__PASSWORD__')
    return session
