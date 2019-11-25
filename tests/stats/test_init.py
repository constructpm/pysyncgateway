

from pysyncgateway import Stats


def test(admin_client):
    result = Stats(admin_client)

    assert result.client == admin_client
    assert result.url.endswith('/_expvar')
    assert result.data == {}
