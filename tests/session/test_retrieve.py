from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import UserClient
from pysyncgateway.exceptions import DoesNotExist

no_auth_response = {
    'authentication_handlers': ['default', 'cookie'],
    'ok': True,
    'userCtx': {
        'channels': {},
        'name': None
    },
}


def test_admin(database):
    session = database.get_session()

    result = session.retrieve()

    assert result is True
    assert session.data == no_auth_response


def test_admin_no_database(admin_client):
    session = admin_client.get_database('db').get_session()

    with pytest.raises(DoesNotExist):
        session.retrieve()


def test_user_no_auth_no_database(syncgateway_public_url):
    user_client = UserClient(syncgateway_public_url)
    session = user_client.get_database('db').get_session()

    with pytest.raises(DoesNotExist):
        session.retrieve()


def test_user_no_auth(database, syncgateway_public_url):
    user_client = UserClient(syncgateway_public_url)
    session = user_client.get_database('db').get_session()

    result = session.retrieve()

    assert result is True
    assert session.data == no_auth_response


def test_user_authed(database, syncgateway_public_url):
    user_client = UserClient(syncgateway_public_url)
    session = user_client.get_database('db').get_session()
    user = database.get_user('__USERNAME__')
    user.set_password('__PASSWORD__')
    user.set_admin_channels('a', 'b', 'c')
    user.create_update()
    user_client.auth('__USERNAME__', '__PASSWORD__')

    result = session.retrieve()

    assert result is True
    assert session.data == {
        'authentication_handlers': ['default', 'cookie'],
        'ok': True,
        'userCtx': {
            'channels': {
                '!': 1,
                'a': 1,
                'b': 1,
                'c': 1,
            },
            'name': '__USERNAME__',
        },
    }
