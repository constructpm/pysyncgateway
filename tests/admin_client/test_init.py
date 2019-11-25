

from pysyncgateway import AdminClient


def test(syncgateway_admin_url):
    result = AdminClient(syncgateway_admin_url)

    assert result.url == syncgateway_admin_url
    assert result._auth is None
