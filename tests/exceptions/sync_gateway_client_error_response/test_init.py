from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway.exceptions import SyncGatewayClientErrorResponse


def test():
    result = SyncGatewayClientErrorResponse(
        400, {
            'error': 'Bad Request',
            'reason': 'Empty passwords are not allowed ',
        }
    )

    assert result.status_code == 400
    assert result.json == {
        'error': 'Bad Request',
        'reason': 'Empty passwords are not allowed ',
    }
