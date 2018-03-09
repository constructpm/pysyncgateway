from __future__ import absolute_import, print_function, unicode_literals

import functools

from requests import ConnectionError

from .exceptions import DoesNotExist, GatewayDown


class ComparableMixin:
    """
    Alex Martelli's suggestion from https://stackoverflow.com/a/1061350/1286705
    """

    def __eq__(self, other):
        return not self < other and not other < self

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self


def sg_method(func, *args, **kwargs):
    """
    Wrap a normal request Verb in GatewayDown and DoesNotExist logic

    Raises:
        GatewayDown: If SyncGateway can't be reached.
        DoesNotExist: If a 404 was received for a request.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except ConnectionError as ce:
            raise GatewayDown(ce.message)
        if response.status_code == 404:
            raise DoesNotExist('{} not found'.format(response.url))
        return response

    return wrapper
