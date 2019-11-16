from collections import namedtuple


Name = namedtuple("Name", ["name", "nick_names", "default_names"])

DeviceInfo = namedtuple(
    "DeviceInfo", ["manufacturer", "modell", "hwVersion", "swVersion"]
)


class Device(object):
    def __init__(
        self,
        id,
        type_,
        traits,
        name,
        device_info,
        room_hint,
        will_report_state=True,
        attributes=None,
        custom_data=None,
    ):
        self.id = id
        self.type = type_
        self.traits = traits
        self.name = name
        self.device_info = device_info
        self.room_hint = room_hint
        self.will_report_state = will_report_state
        self.attributes = attributes
        self.custom_data = custom_data

    def to_json(self):
        ret = {
            "id": self.id,
            "type": self.type,
            "traits": self.traits,
            "name": self.name._asdict(),
            "willReportState": self.will_report_state,
            "deviceInfo": self.device_info._asdict(),
            "roomHint": self.room_hint,
        }
        if self.attributes:
            ret["attributes"] = self.attributes
        if self.custom_data:
            ret["customData"] = self.custom_data
        return ret
