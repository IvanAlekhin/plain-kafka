import marshmallow
import marshmallow_dataclass
from dataclasses import dataclass, field

from plain_kafka.consumer import _decode_msg_value
from plain_kafka.producer import _encode_msg


@dataclass
class SomeEntity:
    test_str: str
    test_int: int
    test_dict: dict


@marshmallow_dataclass.dataclass(base_schema=marshmallow.Schema)
class SomeMDEntity:
    test_str: str = field(metadata=dict(required=True, allow_none=False, description="Error description"))
    test_int: int = field(metadata=dict(required=True, allow_none=False, description="Error description"))
    test_dict: dict = field(metadata=dict(required=True, allow_none=False, description="Error description"))


def check_msg(val):
    encoded = _encode_msg(val)
    if not isinstance(_encode_msg(val), str):
        return False
    decoded = _decode_msg_value(encoded)
    return isinstance(decoded, dict) or isinstance(decoded, str)


def test_serialise_dict():
    val = dict(privet=1,
               poka='kaka')
    assert check_msg(val) is True


def test_serialise_str():
    val = 'sdkfjasldfkj sadf fa'
    assert check_msg(val) is True


def test_serialise_dataclass():
    val = SomeEntity(test_dict=dict(a=1), test_int=3, test_str='sdfakj')
    assert check_msg(val) is True


def test_serialise_marshmallow_dataclass():
    val = SomeMDEntity(test_dict=dict(a=1), test_int=3, test_str='sdfakj')
    assert check_msg(val) is True
