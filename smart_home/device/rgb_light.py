from smart_home.device import Device
from smart_home.device import DeviceInfo
from smart_home.device import Name

from smart_home.device import DEVICE_TYPE_LIGHT

from smart_home.device import DEVICE_TRAITS_BRIGHTNESS
from smart_home.device import DEVICE_TRAITS_COLOR_SETTING
from smart_home.device import DEVICE_TRAITS_ON_OFF


class RGBLight(Device):
    def __init__(
        self, id_, name, nicknames, default_names, device_info, room_hint, obj=None
    ):
        super().__init__(
            id_,
            DEVICE_TYPE_LIGHT,
            [
                DEVICE_TRAITS_BRIGHTNESS,
                DEVICE_TRAITS_COLOR_SETTING,
                DEVICE_TRAITS_ON_OFF,
            ],
            Name(name, nicknames, default_names),
            device_info,
            room_hint,
            attributes={"colorModel": "rgb"},
            obj=obj,
        )
