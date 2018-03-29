from __future__ import absolute_import, print_function, unicode_literals


class PysyncgatewayException(Exception):
    """
    The root of all Evil >:D
    """


class ClientUnauthorized(PysyncgatewayException):
    """
    Client is not authorized to access this URL
    """


class GatewayDown(PysyncgatewayException):
    """
    SyncGateway could not be reached on configured URL
    """


class InvalidChannelName(PysyncgatewayException):
    pass


class InvalidDataKey(PysyncgatewayException):
    pass


class InvalidDatabaseName(PysyncgatewayException):
    pass


class InvalidDocumentID(PysyncgatewayException):
    pass


class InvalidPassword(PysyncgatewayException):
    pass


class DoesNotExist(PysyncgatewayException):
    """
    Generic exception to replace 404s. Used if databases, users or documents
    can't be loaded.
    """


class NotLoaded(PysyncgatewayException):
    """
    Item from a ``Resources`` data attribute was requested, but that resource
    has not yet been successfully retrieved from Sync Gateway.
    """


class RevisionMismatch(PysyncgatewayException):
    pass


class SyncGatewayClientErrorResponse(PysyncgatewayException):
    """
    Sync gateway responded with a 4xx error.

    Attributes:
        status_code (int): Error code in the response from sync gateway.
        json (dict): Body of response from sync gateway.
    """

    def __init__(self, status_code, json):
        self.status_code = status_code
        self.json = json

    @classmethod
    def from_response(obj, response):
        """
        Args:
            response (requests.Response)

        Returns:
            SyncGatewayClientErrorResponse
        """
        return obj(response.status_code, response.json())

    def __repr__(self):
        """
        Returns:
            str
        """
        return '<SyncGatewayClientErrorResponse {}>'.format(self)

    def __str__(self):
        """
        Used by pytest to show stack trace.

        Returns:
            str: Containing `status_code` and `json['error']`.
        """
        return '{} "{}"'.format(self.status_code, self.json['error'])
