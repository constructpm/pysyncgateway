import pytest

from pysyncgateway import AdminClient


def test_eq(admin_client, syncgateway_admin_url):
    other = AdminClient(syncgateway_admin_url)

    result = admin_client == other

    assert result is True


def test_neq(admin_client):
    other = AdminClient('http://example.com/')

    result = admin_client == other

    assert result is False


# --- FAILURES ---


def test_other_type(admin_client):
    with pytest.raises(ValueError) as excinfo:
        admin_client < 1

    assert 'int' in excinfo.value.args[0]
