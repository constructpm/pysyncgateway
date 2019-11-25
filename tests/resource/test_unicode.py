# encoding: utf-8


from pysyncgateway import Database
from pysyncgateway.resource import Resource


def test(admin_client):
    """
    This indirectly tests Resource.__repr__
    """
    database = Database(admin_client, 'db')
    resource = Resource(database)
    resource.url = 'http://mockhőst/db/__Café__'

    result = str(resource)

    assert result == '<Resource "http://mockhőst/db/__Café__">'
