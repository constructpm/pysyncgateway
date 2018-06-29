from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway.exceptions import DoesNotExist


def test(existing_user):
    result = existing_user.delete()

    assert result is True
    assert existing_user.retrieved is False
    with pytest.raises(DoesNotExist):
        existing_user.retrieve()


def test_retrieved(existing_user):
    existing_user.retrieve()

    result = existing_user.delete()

    assert result is True
    assert existing_user.retrieved is False
    with pytest.raises(DoesNotExist):
        existing_user.retrieve()


# --- FAILURES ---


def test_missing_user(user):
    with pytest.raises(DoesNotExist):
        user.delete()


def test_missing_database(admin_client):
    user = admin_client.get_database('db').get_user('test-user')

    with pytest.raises(DoesNotExist):
        user.delete()
