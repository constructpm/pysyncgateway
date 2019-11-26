import pytest

from pysyncgateway import Database
from pysyncgateway.exceptions import SyncGatewayClientErrorResponse


def test(admin_client):
    database = Database(admin_client, 'test_newnewdb')

    result = database.create()

    assert result is True
    assert database in admin_client.all_databases()


# --- FAILURES ---


def test_collision(admin_client):
    """
    Database can't be created if already exists
    """
    existing_database = admin_client.get_database('test_collision')
    existing_database.create()

    with pytest.raises(SyncGatewayClientErrorResponse) as excinfo:
        admin_client.get_database('test_collision').create()

    assert 'Duplicate database name' in excinfo.value.json['reason']
