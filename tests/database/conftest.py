from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import AdminClient


@pytest.fixture
def admin_client(syncgateway_admin_url):
    """
    Returns:
        AdminClient: Pointed at default admin URL.
    """
    return AdminClient(syncgateway_admin_url)
