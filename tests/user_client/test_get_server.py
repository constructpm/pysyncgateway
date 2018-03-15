from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import UserClient

# --- FAILURES ---


def test_no_auth(syncgateway_public_url):
    user_client = UserClient(syncgateway_public_url)

    user_client.get_server()
