from __future__ import absolute_import, print_function, unicode_literals

from pysyncgateway.exceptions import SyncGatewayClientErrorResponse


def test():
    exception = SyncGatewayClientErrorResponse(
        400, {
            'error': 'Bad Request',
            'reason': 'Empty passwords are not allowed ',
        }
    )

    result = repr(exception)

    assert result == '<SyncGatewayClientErrorResponse 400 "Bad Request">'
