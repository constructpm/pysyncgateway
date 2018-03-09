from __future__ import absolute_import, print_function, unicode_literals


def test(admin_client):
    result = admin_client.get_server()

    assert isinstance(result, dict)
    assert list(result) == ['ADMIN', 'couchdb', 'vendor', 'version']
    assert result['ADMIN'] is True
    assert result['version'] == 'Couchbase Sync Gateway/1.5.1(4;cb9522c)'
