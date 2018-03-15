from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import User
from pysyncgateway.exceptions import DoesNotExist, SyncGatewayClientErrorResponse


def test_happy(user, database, admin_client):
    user.set_password('vas62#4nf')

    result = user.create_update()

    assert result == admin_client.CREATED
    assert database.all_users() == [user]


def test_create_user_channels(user, database, admin_client):
    user.set_password('vas62#4nf')
    user.set_admin_channels('creator.test', 'approval.test.1234')

    result = user.create_update()

    assert result == admin_client.CREATED
    assert database.all_users() == [user]


# --- FAILURES ---


def test_no_password(user):
    with pytest.raises(SyncGatewayClientErrorResponse) as excinfo:
        user.create_update()

    assert excinfo.value.status_code == 400
    assert excinfo.value.json['reason'] == 'Empty passwords are not allowed '  # NOTE trailing whitespace


def test_no_database(admin_client):
    missing_db = admin_client.get_database('not_db')
    new_user = User(missing_db, 'user')
    new_user.set_password('__PASSWORD__')

    with pytest.raises(DoesNotExist):
        new_user.create_update()
