from collections import namedtuple


DEVICE_TYPE_OUTLET = "action.devices.types.OUTLET"
DEVICE_TYPE_LIGHT = "action.devices.types.LIGHT"


DEVICE_TRAITS_BRIGHTNESS = "action.devices.traits.Brightness"
DEVICE_TRAITS_COLOR_SETTING = "action.devices.traits.ColorSetting"
DEVICE_TRAITS_ON_OFF = "action.devices.traits.OnOff"


Name = namedtuple("Name", ["name", "nicknames", "defaultNames"])

DeviceInfo = namedtuple(
    "DeviceInfo", ["manufacturer", "model", "hwVersion", "swVersion"]
)


class Device(object):
    def __init__(
        self,
        id_,
        type_,
        traits,
        name,
        device_info,
        room_hint,
        will_report_state=True,
        attributes=None,
        custom_data=None,
        obj=None,
    ):
        self.id = id_
        self.type = type_
        self.traits = traits
        self.name = name
        self.device_info = device_info
        self.room_hint = room_hint
        self.will_report_state = will_report_state
        self.attributes = attributes
        self.custom_data = custom_data
        self.obj = obj

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


from .rgb_light import RGBLight
