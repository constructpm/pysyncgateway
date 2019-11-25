

from pysyncgateway import AdminClient, Database


def test():
    admin_client = AdminClient('http://example.com:4985/')
    database = Database(admin_client, 'test')

    result = str(database)

    assert result == '<Database "http://example.com:4985/test/">'
