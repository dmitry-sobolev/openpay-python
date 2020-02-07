from .models import ErrorModel


class ErrorCodes:
    SVV2_IS_NOT_PROVIDED = 2006
    INSUFFICIENT_FUNDS = 3003


# Exceptions
class OpenpayError(Exception):
    prefix = 'Openpay'

    def __init__(self, message=None, err: ErrorModel = None, http_body=None, http_status=None,
                 json_body=None):
        super(OpenpayError, self).__init__(f'{self.prefix}: {message}')

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf=8')
            except:
                http_body = ('<Could not decode body as utf-8. '
                             'Please report to support@openpay.mx>')

        self.http_body = http_body

        self.http_status = http_status
        self.json_body = json_body
        self.err = err


class APIError(OpenpayError):
    pass


class APIConnectionError(OpenpayError):
    pass


class CardError(OpenpayError):

    def __init__(self, message, err: ErrorModel, param, code, http_body=None,
                 http_status=None, json_body=None):
        super(CardError, self).__init__(message, err,
                                        http_body, http_status, json_body)

        self.param = param
        self.code = code


class InvalidRequestError(OpenpayError):

    def __init__(self, message, err: ErrorModel, param, http_body=None,
                 http_status=None, json_body=None):
        super(InvalidRequestError, self).__init__(
            message, err, http_body, http_status, json_body)
        self.param = param


class AuthenticationError(OpenpayError):
    pass
