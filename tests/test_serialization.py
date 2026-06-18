import base64
from types import SimpleNamespace

from rosboard.serialization import dict2ros


class ScalarMessage:
    __slots__ = ("count", "enabled", "label")

    def __init__(self):
        self.count = 0
        self.enabled = False
        self.label = ""


class BytesMessage:
    __slots__ = ("payload",)

    def __init__(self):
        self.payload = b""


class ChildMessage:
    __slots__ = ("count",)

    def __init__(self):
        self.count = 0


class ParentMessage:
    __slots__ = ("child",)

    def __init__(self):
        self.child = ChildMessage()


class SequenceElement:
    __slots__ = ("count",)

    def __init__(self):
        self.count = 0


class SequenceMessage:
    def __init__(self):
        self.items = []

    def get_fields_and_field_types(self):
        return {"items": "sequence<fake_pkg/msg/SequenceElement>"}


def test_dict2ros_coerces_scalar_field_types():
    msg = dict2ros({"count": "7", "enabled": 1, "label": 9}, ScalarMessage)

    assert msg.count == 7
    assert msg.enabled is True
    assert msg.label == "9"


def test_dict2ros_leaves_uncoercible_scalars_unchanged():
    msg = dict2ros({"count": "not-an-int"}, ScalarMessage)

    assert msg.count == "not-an-int"


def test_dict2ros_decodes_base64_bytes_fields():
    encoded = base64.b64encode(b"abc").decode()

    msg = dict2ros({"payload": encoded}, BytesMessage)

    assert msg.payload == b"abc"


def test_dict2ros_recurses_into_nested_messages():
    msg = dict2ros({"child": {"count": "5"}}, ParentMessage)

    assert isinstance(msg.child, ChildMessage)
    assert msg.child.count == 5


def test_dict2ros_deserializes_ros2_message_sequences(monkeypatch):
    def fake_import_module(name):
        assert name == "fake_pkg.msg"
        return SimpleNamespace(SequenceElement=SequenceElement)

    monkeypatch.setattr("rosboard.serialization.importlib.import_module", fake_import_module)

    msg = dict2ros({"items": [{"count": "3"}]}, SequenceMessage)

    assert len(msg.items) == 1
    assert isinstance(msg.items[0], SequenceElement)
    assert msg.items[0].count == 3


def test_dict2ros_keeps_mixed_lists_as_plain_values():
    msg = dict2ros({"items": [{"count": "3"}, "raw"]}, SequenceMessage)

    assert msg.items == [{"count": "3"}, "raw"]
