from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway import AdminClient, Database


def test():
    admin_client = AdminClient('http://example.com:4985/')
    database = Database(admin_client, 'test')

    result = str(database)

    assert result == '<Database "http://example.com:4985/test/">'
