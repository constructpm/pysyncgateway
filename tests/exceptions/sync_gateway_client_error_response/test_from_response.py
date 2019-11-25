import pytest
from requests import get

from pysyncgateway.exceptions import SyncGatewayClientErrorResponse


@pytest.fixture
def response(admin_client):
    """
    Returns:
        requests.Response: A 404 response.
    """
    return get('{}/missing'.format(admin_client.url))


def test_response(response):
    result = response

    assert result.status_code == 404


def test(response):
    result = SyncGatewayClientErrorResponse.from_response(response)

    assert result.status_code == 404
    assert result.json == {
        'error': 'not_found',
        'reason': 'unknown URL',
    }
