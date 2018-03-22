from __future__ import absolute_import, print_function, unicode_literals

import pytest
import responses

from pysyncgateway import Stats
from pysyncgateway.exceptions import GatewayDown


def test(admin_client):
    stats = Stats(admin_client)

    result = stats.retrieve()

    assert result is True
    assert sorted(list(stats.data)) == [
        'cb',
        'cmdline',
        'goroutine_stats',
        'mc',
        'memstats',
        'syncGateway_changeCache',
        'syncGateway_db',
        'syncGateway_dcp',
        'syncGateway_gocb',
        'syncGateway_httpListener',
        'syncGateway_index',
        'syncGateway_index_clocks',
        'syncGateway_rest',
        'syncGateway_stats',
    ]


@responses.activate
def test_bad_json(admin_client):
    """
    expvars endpoint returns something non-JSON nasty, raises ValueError
    """
    stats = Stats(admin_client)
    responses.add(responses.GET, stats.url, body=':D')

    with pytest.raises(ValueError):
        stats.retrieve()


@responses.activate
def test_missing_endpoint(admin_client):
    """
    expvars endpoint goes AWOL
    """
    stats = Stats(admin_client)

    with pytest.raises(GatewayDown):
        stats.retrieve()
