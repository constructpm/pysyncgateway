from __future__ import absolute_import, print_function, unicode_literals

import functools
import re

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


def assert_valid_database_name(name):
    """
    Raise exception if database name does not match Couchbase requirements

    From docs: http://docs.couchdb.org/en/stable/api/database/common.html#put--db

    > The database name must begin with a lowercase letter.
    > The database name must contain only valid characters. The following
    > characters are valid in database names:
    > Lowercase letters: a-z
    > Numbers: 0-9
    > Special characters: _$()+-/

    NOTE hyphen is allowed, compared to channel names below.

    0.  Empty string is invalid
    >>> assert_valid_database_name('')
    Traceback (most recent call last):
    ...
    AssertionError: Empty database name is not allowed

    1.  Special-special characters are not allowed.
    >>> assert_valid_database_name('stuff!db')
    Traceback (most recent call last):
    ...
    AssertionError: Special characters are not allowed in database names, first bad character is "!"

    2.  White space is not allowed.
    >>> assert_valid_database_name('db 2')
    Traceback (most recent call last):
    ...
    AssertionError: Special characters are not allowed in database names, first bad character is " "

    3.  Capitals are not allowed
    >>> assert_valid_database_name('bIGdATA')
    Traceback (most recent call last):
    ...
    AssertionError: Special characters are not allowed in database names, first bad character is "I"

    4.  Must start with a letter
    >>> assert_valid_database_name('-10degrees')
    Traceback (most recent call last):
    ...
    AssertionError: Database names must start with a lowercase letter

    4.  Happy 'simple' database names are OK
    >>> assert_valid_database_name('construct-pm($)//x_x')
    """
    assert name > '', 'Empty database name is not allowed'
    assert re.match(r'^[a-z]', name), 'Database names must start with a lowercase letter'

    character_error_msg = 'Special characters are not allowed in database names, first bad character is "{}"'
    valid_db_name = re.match(r'^[a-z0-9\+\-\(\)\$/_]*', name).group()

    assert valid_db_name == name, character_error_msg.format(name[len(valid_db_name)])
