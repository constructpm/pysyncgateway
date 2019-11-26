import pytest

from pysyncgateway import UserClient
from pysyncgateway.exceptions import ClientUnauthorized

# Only public API endpoints that require auth are on a database, so use a
# database here to assert that auth is working.


@pytest.fixture
def user_client(syncgateway_public_url):
    """
    Returns:
        UserClient: Pointed at test public URL.
    """
    return UserClient(syncgateway_public_url)


@pytest.fixture
def database(admin_client):
    """
    Returns:
        Database: 'auth_test' database written to Sync Gateway.
    """
    database = admin_client.get_database("auth_test")
    database.create()
    return database


@pytest.fixture
def user_client_database(database, user_client):
    """
    Returns:
        Database: Named 'auth_test', with ``user_client`` set as the client in
        an unauthed state.
    """
    return user_client.get_database("auth_test")


def test_user_client_database(user_client_database):
    """
    user_client_database provides an unauthorized client.
    """
    result = user_client_database

    with pytest.raises(ClientUnauthorized):
        result.get()


@pytest.fixture
def user(database):
    """
    Returns:
        User: 'test_user' in 'auth_test' database written to Sync Gateway.
    """
    user = database.get_user("test_user")
    user.set_password("__PASSWORD__")
    user.create_update()
    return user


def test_user(user, database):
    result = user

    assert result in database.all_users()


# --- TESTS ---


def test(user, user_client, user_client_database):
    """
    Setting auth on UserClient allows access to Database.
    """
    result = user_client.auth("test_user", "__PASSWORD__")

    assert result is None
    assert user_client_database.get()["db_name"] == "auth_test"


# --- FAILURES ---


def test_bad_auth(user, user_client, user_client_database):
    """
    Incorrect credentials are only tested when making a subsequent request.
    """
    result = user_client.auth("test_user", "OTHER_PASSWORD")

    assert result is None
    with pytest.raises(ClientUnauthorized):
        user_client_database.get()
