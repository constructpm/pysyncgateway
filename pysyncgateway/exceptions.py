from __future__ import absolute_import, print_function, unicode_literals


class PysyncgatewayException(Exception):
    """
    The root of all Evil >:D
    """


class GatewayDown(PysyncgatewayException):
    """
    SyncGateway could not be reached on configured URL
    """


class InvalidChannelName(PysyncgatewayException):
    pass


class InvalidDatabaseName(PysyncgatewayException):
    pass


class InvalidDocumentID(PysyncgatewayException):
    pass


class DoesNotExist(PysyncgatewayException):
    """
    Generic exception to replace 404s. Used if databases, users or documents
    can't be loaded.
    """
