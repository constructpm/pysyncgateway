from __future__ import absolute_import, print_function, unicode_literals

import pytest

from pysyncgateway import AdminClient


@pytest.fixture
def syncgateway_admin_url():
    """
    Returns:
        str: URL to reach admin port of SG.
    """
    return 'http://localhost:4985/'


@pytest.fixture
def syncgateway_public_url():
    """
    Returns:
        str: URL to reach public SG.
    """
    return 'http://localhost:4985/'


@pytest.fixture
def cleanup_databases():
    """
    Returns:
        bool: admin_client fixture should ignore any existing databases at
            start of test and clean them up.
    """
    return True


@pytest.fixture
def admin_client(syncgateway_admin_url, cleanup_databases):
    """
    Returns:
        AdminClient: Pointed at default admin API URL. Asserts that there are
            no databases at the start of test. Deletes all databases at end of
            test.
    """
    admin_client = AdminClient(syncgateway_admin_url)

    if cleanup_databases:
        purge_databases(admin_client)

    all_databases = admin_client.all_databases()
    assert len(all_databases) == 0, (
        'Test initialised with {} unexpected Databases {}. '
        'Try setting `cleanup_databases` fixture to `True`?'.format(len(all_databases), all_databases)
    )

    yield admin_client

    purge_databases(admin_client)


def purge_databases(admin_client):
    for database in admin_client.all_databases():
        database.delete()
