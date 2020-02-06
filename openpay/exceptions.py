class APIValidateException(Exception):

    status_code = 400

    def __init__(self, field: str, error: str):
        message = f'`{field}`: {str(error)} '

        if isinstance(error, str) and error.find('%s') != -1:
            message = error % field

        super().__init__(message)
