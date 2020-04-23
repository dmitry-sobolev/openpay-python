from typing import Dict

from marshmallow import Schema, fields, post_dump
from .exceptions import APIValidateException


class WrappedStruct(object):

    def _import(self, data: dict):
        for name, value in data.items():
            if name[:1] == '_':
                continue
            setattr(self, name.replace('-', '_'), self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            if isinstance(value, dict):
                struct = WrappedStruct()
                struct._import(value)
                return struct
            else:
                return value

    def dict_value(self) -> dict:
        return self.__dict__

    def dict_value_deep(self) -> dict:
        result = self.dict_value()
        for name, value in result.items():
            if isinstance(value, WrappedStruct):
                result[name] = value.dict_value_deep()
            else:
                result[name] = value
        return result

    def __iter__(self):
        for attr in self.__dict__.keys():
            yield attr



class BaseModel(WrappedStruct):
    __schema__ = Schema

    def __init__(self, params: dict):
        data = self._validate(params)
        self._import(data)
        self._post_validate()

    def _validate(self, params) -> dict:
        schema = self.__schema__()
        errors = schema.validate(params)
        self._raise_errors(errors)

        if len(errors) == 0:
            return schema.load(params).data
        else:
            return params

    def _post_validate(self):
        pass

    def _raise_errors(self, errors: Dict[str, list]):
        if len(errors) == 0:
            return

        for field in errors:
            error_message = errors[field]

            if isinstance(error_message, list):
                if len(error_message) != 0:
                    error_message = error_message[0]
                else:
                    error_message = None

            if error_message is None:
                continue

            raise APIValidateException(field, error_message)


class ErrorSchema(Schema):
    category = fields.Str(required=True, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    http_code = fields.Int(required=True, allow_none=False)
    error_code = fields.Int(required=True, allow_none=False)
    request_id = fields.Str(required=False, allow_none=True)
    fraud_rules = fields.List(fields.Str(), required=False, allow_none=True)


class ErrorModel(BaseModel, ErrorSchema):
    __schema__ = ErrorSchema
