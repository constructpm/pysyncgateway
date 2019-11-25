from pysyncgateway import UserClient


def test(syncgateway_public_url):
    result = UserClient(syncgateway_public_url)

    assert result.url == syncgateway_public_url
    assert result._auth is None
