import pytest
from pysyncgateway import AdminClient
from pysyncgateway.exceptions import GatewayDown


def test_empty(admin_client):
    result = admin_client.all_databases()

    assert result == []


def test_happy_multiple(admin_client):
    admin_client.get_database('test_a').create()
    admin_client.get_database('test_b').create()
    admin_client.get_database('test_c').create()

    result = admin_client.all_databases()

    assert sorted(result) == [admin_client.get_database('test_' + n) for n in ('a', 'b', 'c')]


# --- FAILURES ---


def test_server_down():
    bad_client = AdminClient('http://localhost:9999/')

    with pytest.raises(GatewayDown):
        bad_client.all_databases()
