"""
GoodWan client library: serializer
"""

from goodwan_client.errors import ParseError
from goodwan_client.helpers import str_to_datetime


class Serializer:
    def __init__(self, timezone):
        """
        Constructor
        :param timezone: pytz timezone
        :type timezone: pytz.timezone
        """
        self.timezone = timezone

    def objectify(self, data, cls):
        """
        Deserialize data
        :param data: data to objectify
        :type data: dict
        :param cls: class
        :type cls: type
        :return: object of type cls
        """
        if not isinstance(data, dict):
            raise ParseError("Data item is not a dict")

        obj = cls()
        for field, field_parser in cls.__dict__.items():
            if not field.startswith("__"):
                if field not in data:
                    raise ParseError("No \"{}\" field in data item"
                                     .format(field))
                if issubclass(field_parser, ObjectifyField):
                    val = field_parser.parse_data(data[field], self)
                elif hasattr(field_parser, "__call__"):
                    try:
                        val = field_parser(data[field])
                    except Exception as err:
                        raise ValueError("Cannot parse field \"{}\": {}"
                                         .format(field, err))
                else:
                    raise ValueError("Wrong field \"{}\" parser for class {}"
                                     .format(field, cls.__class__.__name__))
                setattr(obj, field, val)

        return obj


class ObjectifyField:
    """ Basic field class for objectify'able class """
    @staticmethod
    def parse_data(data, serializer):
        raise NotImplementedError("Cannot use ObjectifyField class itself")


class DateTimeField(ObjectifyField):
    """ Datetime field for objectify'able class """
    @staticmethod
    def parse_data(data, serializer):
        """
        Parse data
        :param data: data
        :type data: str
        :param serializer: serializer
        :type serializer: Serializer
        """
        return str_to_datetime(data, serializer.timezone)
