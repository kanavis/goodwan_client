"""
GoodWan client library: classes
"""
import datetime
from goodwan_client.serializer import DateTimeField


class Basic:
    """ Basic class """

    def __repr__(self):
        """ Representation """
        return "<{}.{} {}>".format(
            self.__module__,
            self.__class__.__name__,
            ", ".join(
                "{}={}".format(k, v) for k, v in self.__dict__.items()
                if not k.startswith("__")
            )
        )


class Event(Basic):
    """ Event class """
    id_event = int                  # type: int
    id_system = str                 # type: str
    id_transmitter = int            # type: int
    data_type = int                 # type: int
    data = str                      # type: str
    data_ext = str                  # type: str
    signal_lvl = int                # type: int
    timestamp = DateTimeField       # type: datetime.datetime
