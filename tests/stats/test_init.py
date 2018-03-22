from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import Stats


def test(admin_client):
    result = Stats(admin_client)

    assert result.client == admin_client
    assert result.url.endswith('/_expvar')
    assert result.data == {}
