# Actions on Google: Python Smart Home

Python lib to handle the Google Actions

https://developers.google.com/assistant/smarthome/develop/process-intents

# Example

```py
from smart_home import RequestHandler
from smart_home import actions


class MyActionHandler(RequestHandler):
    def __init__(self, led, name, nickname, fullname, room):
        # Provide a list of devices (smart_home.device.Device)
        super().__init__(None, my_list_of_rgb_lights_devices, mapping_from_acitons_to_handlers)
```

Example of mapping from actions to handlers:
```py
from smart_home import actions
{
    actions.ACTION_COMMAND_BRIGHTNESS_ABSOLUTE: self.set_brightness,
    actions.ACTION_COMMAND_COLOR_ABSOLUTE: self.set_color,
    actions.ACTION_COMMAND_ON_OFF: self.set_on_off,
}
```

Then override the `format_device_state(self, device_ids)` method which should format the state of the given device ids

Example:
```py
def format_device_state(self, device_ids):
    device_status = dict()
    for device_id in device_ids:

        device = self.get_device(device_id)

        if not device:
            raise error.RequestError(
                self.current_request_id, error.ERROR_DEVICE_NOT_FOUND
            )

        device_obj = device.obj

        device_status[device_id] = {
            "on": device_obj.is_on,
            "online": True,
            "brightness": round(device_obj.brightness * 100.0),
            "color": {"spectrumRGB": device_obj.color_rgb_spectrum},
        }
    return device_status
```

## License
See [LICENSE](LICENSE).