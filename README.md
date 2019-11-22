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
        super().__init__(None, my_list_of_rgb_lights_devices)
        # List all actions you want to support
        self.execute_handlers = {
            actions.ACTION_COMMAND_BRIGHTNESS_ABSOLUTE: self._set_brightness,
            actions.ACTION_COMMAND_COLOR_ABSOLUTE: self._set_color,
            actions.ACTION_COMMAND_ON_OFF: self._set_on_off,
        }
```

Then override the two `handle_query_request`, `handle_execute_request` methods to implement your logic and return a dict using the `format_query_response` and `format_execute_response` respectively.

Example of EXECUTE request:
```py
def handle_execute_request(self, input_data):
    commands = input_data["payload"]["commands"]

    return_payload = dict()
    for command in commands:
        # Get the devices...
        devices = command["devices"]
        # ...and the executions
        executions = command["execution"]
        # Loop all devices
        for device in devices:
            device = self.get_device(device["id"])

            # Loop all executions for each device
            for execution in executions:
                exec_command = execution["command"]
                params = execution["params"]

                if exec_command not in self.execute_handlers:
                    raise error.RequestError(
                        self.current_request_id, error.ERROR_NOT_SUPPORTED
                    )

                self.execute_handlers[exec_command](return_payload, device, params)
                
    return self.format_execute_response(return_payload)
```

## License
See [LICENSE](LICENSE).