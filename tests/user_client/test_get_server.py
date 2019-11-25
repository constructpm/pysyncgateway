from pysyncgateway import UserClient


def test(syncgateway_public_url):
    user_client = UserClient(syncgateway_public_url)

    result = user_client.get_server()

    assert sorted(list(result)) == ["couchdb", "vendor", "version"]  # No ADMIN key
