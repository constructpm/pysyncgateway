from __future__ import absolute_import, print_function, unicode_literals

import pytest


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
