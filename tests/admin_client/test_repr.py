from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import AdminClient


def test(syncgateway_admin_url):
    admin_client = AdminClient(syncgateway_admin_url)

    result = str(admin_client)

    assert result == '<AdminClient on "http://localhost:4985/">'
