from __future__ import absolute_import, print_function, unicode_literals

import functools
import re

from requests import ConnectionError

from .exceptions import (
    ClientUnauthorized,
    DoesNotExist,
    GatewayDown,
    InvalidChannelName,
    InvalidDatabaseName,
    InvalidDocumentID,
    RevisionMismatch,
    SyncGatewayClientErrorResponse,
)


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
    Wrap a normal request Verb (E.g. `requests.get`) in exception handling
    logic.

    Raises:
        DoesNotExist: If a 404 was received for a request.
        GatewayDown: If SyncGateway can't be reached.
        SyncGatewayClientErrorResponse: When any "not OK" response (according
            to `requests.Response.ok` is received that is not a 404.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except ConnectionError as ce:
            raise GatewayDown(ce.message)

        if response.status_code == 401:
            raise ClientUnauthorized(response.json()['reason'])
        elif response.status_code == 404:
            raise DoesNotExist('{} not found'.format(response.url))
        elif response.status_code == 409:
            raise RevisionMismatch()
        if not response.ok:
            raise SyncGatewayClientErrorResponse.from_response(response)
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
    InvalidDatabaseName: Empty database name is not allowed

    1.  Special-special characters are not allowed.
    >>> assert_valid_database_name('stuff!db')
    Traceback (most recent call last):
    ...
    InvalidDatabaseName: Special characters are not allowed in database names, first bad character is "!"

    2.  White space is not allowed.
    >>> assert_valid_database_name('db 2')
    Traceback (most recent call last):
    ...
    InvalidDatabaseName: Special characters are not allowed in database names, first bad character is " "

    3.  Capitals are not allowed
    >>> assert_valid_database_name('bIGdATA')
    Traceback (most recent call last):
    ...
    InvalidDatabaseName: Special characters are not allowed in database names, first bad character is "I"

    4.  Must start with a letter
    >>> assert_valid_database_name('-10degrees')
    Traceback (most recent call last):
    ...
    InvalidDatabaseName: Database names must start with a lowercase letter

    4.  Happy 'simple' database names are OK
    >>> assert_valid_database_name('construct-pm($)//x_x')
    """
    if not name:
        raise InvalidDatabaseName('Empty database name is not allowed')

    if not re.match(r'^[a-z]', name):
        raise InvalidDatabaseName('Database names must start with a lowercase letter')

    valid_db_name = re.match(r'^[a-z0-9\+\-\(\)\$/_]*', name).group()
    if valid_db_name == name:
        return

    raise InvalidDatabaseName(
        'Special characters are not allowed in database names, first bad character is "{}"'.format(
            name[len(valid_db_name)]
        )
    )


def assert_valid_document_id(doc_id):
    """
    NOTE this could become prohibitive if the admin client can't delete
    documents that fall outside the boundaries of the set of allowed names.
    E.g. App creates bad document and admin needs to clean it up, but can't.
    Therefore this validation should only be used on creation.

    0.  Empty string is invalid
    >>> assert_valid_document_id('')
    Traceback (most recent call last):
    ...
    InvalidDocumentID: Empty document id is not allowed

    1.  Colon is not allowed in document id
    >>> assert_valid_document_id('colon:nope')
    Traceback (most recent call last):
    ...
    InvalidDocumentID: Colon is not allowed in document ids

    1.5 Question mark is not allowed (this is allowed in couchbase, but would
        require much urlencoding and mashing to get working via python IMO so
        banning it for now)
        If trying to quote, then `quote(doc_id, safe='')` will raise `KeyError`
        and Hell's Armies walk the earth.
    >>> assert_valid_document_id('Questions? Nope')
    Traceback (most recent call last):
    ...
    InvalidDocumentID: Question mark is not allowed in document ids

    1.6 Hash banned for the same reason as question mark.
    >>> assert_valid_document_id('hashes### like a boss')
    Traceback (most recent call last):
    ...
    InvalidDocumentID: Hash is not allowed in document ids

    2.  Special-special characters are allowed, and can start the doc id.
    >>> assert_valid_document_id('$stuff!channel')

    3.  White space is allowed.
    >>> assert_valid_document_id('channel 2')

    4.  Loads of special characters are OK
    >>> assert_valid_document_id('*-=|+/.,@(1234)')
    """
    if not doc_id:
        raise InvalidDocumentID('Empty document id is not allowed')

    for char, name in [(':', 'Colon'), ('?', 'Question mark'), ('#', 'Hash')]:
        if char in doc_id:
            raise InvalidDocumentID('{} is not allowed in document ids'.format(name))


def assert_valid_channel_name(name):
    """
    Assert channel name passes sync gateway's requirements.

    > Valid channel names consist of letter [A-Z, a-z], digits [0-9], and a few
    > special characters [= + / . , _ @]. The empty string is not allowed. The
    > special channel name * denotes all channels.

    Docs are out of date: https://github.com/couchbase/sync_gateway/issues/656
    Therefore adding '-' as allowed.

    Args:
        name (str)

    Raises:
        InvalidChannelName

    0.  Empty string is invalid
    >>> assert_valid_channel_name('')
    Traceback (most recent call last):
    ...
    InvalidChannelName: Empty channel name is not allowed

    1.  Special-special characters are not allowed.
    >>> assert_valid_channel_name('stuff!channel')
    Traceback (most recent call last):
    ...
    InvalidChannelName: Special characters are not allowed in channels, first bad character is "!"

    2.  White space is not allowed.
    >>> assert_valid_channel_name('channel 2')
    Traceback (most recent call last):
    ...
    InvalidChannelName: Special characters are not allowed in channels, first bad character is " "

    3.  When bad character matches at start of line, it's found
    >>> assert_valid_channel_name('$1 channel')
    Traceback (most recent call last):
    ...
    InvalidChannelName: Special characters are not allowed in channels, first bad character is "$"

    4.  When name is just bad characters, first bad char is returned
    >>> assert_valid_channel_name('#&()`')
    Traceback (most recent call last):
    ...
    InvalidChannelName: Special characters are not allowed in channels, first bad character is "#"

    5.  Some special characters are OK
    >>> assert_valid_channel_name('-ISG_project=+/.,@1234')
    """
    if not name:
        raise InvalidChannelName('Empty channel name is not allowed')

    valid_channel_name = re.match(r'^[A-Za-z0-9=\+\-/\.,_@]*', name).group()

    if valid_channel_name == name:
        return

    raise InvalidChannelName(
        'Special characters are not allowed in channels, first bad character is "{}"'.format(
            name[len(valid_channel_name)]
        )
    )
