import pytest
from pysyncgateway.exceptions import DoesNotExist


def test_happy(existing_user):
    result = existing_user.retrieve()

    assert result is True
    assert existing_user.data == {
        'name': 'test-user',
        'admin_channels': ['approval.test.1234', 'creator.test'],
        'all_channels': ['!', 'approval.test.1234', 'creator.test'],
    }
    assert existing_user.admin_channels == ('approval.test.1234', 'creator.test')
    assert existing_user.retrieved is True


def test_no_admin_channels(user):
    user.set_password('__PASSWORD__')
    user.create_update()
    user.set_admin_channels('channel.set.after.create')

    result = user.retrieve()

    assert result is True
    assert user.admin_channels == ()
    assert user.retrieved is True


# --- FAILURES ---


def test_missing_user(user):
    user.data = {
        'stuff': 'old data',
    }

    with pytest.raises(DoesNotExist):
        user.retrieve()

    assert user.data == {}
    assert user.retrieved is False


def test_missing_database(admin_client):
    user = admin_client.get_database('db').get_user('test-user')

    with pytest.raises(DoesNotExist):
        user.retrieve()
