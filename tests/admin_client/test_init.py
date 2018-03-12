from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import AdminClient


def test(syncgateway_admin_url):
    result = AdminClient(syncgateway_admin_url)

    assert result.url == syncgateway_admin_url
