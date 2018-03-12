from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import AdminClient


@pytest.fixture
def admin_client(syncgateway_admin_url):
    """
    Returns:
        AdminClient: Pointed at default admin URL. Deletes all databases at end
            of test.
    """
    admin_client = AdminClient(syncgateway_admin_url)
    yield admin_client
    for database in admin_client.all_databases():
        database.delete()
