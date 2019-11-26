import pytest

from pysyncgateway import AdminClient, Database


def test(admin_client):
    result = Database(admin_client, 'test')

    assert result.client == admin_client
    assert result.name == 'test'
    assert result.url == 'http://localhost:4985/test/'


# --- FAILURES ---


def test_empty_url():
    admin_client = AdminClient('')

    with pytest.raises(ValueError):
        Database(admin_client, 'test')


def test_missing_url():
    with pytest.raises(ValueError):
        Database(1, 'test')
