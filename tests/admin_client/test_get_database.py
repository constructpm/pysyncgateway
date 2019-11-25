

from pysyncgateway import Database


def test(admin_client):
    result = admin_client.get_database('test')

    assert isinstance(result, Database)
    assert result.client == admin_client
    assert result.name == 'test'
