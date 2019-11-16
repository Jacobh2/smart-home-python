from smart_home import error
from smart_home import actions
from smart_home.device import Device
from smart_home.error import RequestError


class RequestHandler(object):
    def __init__(self, agent_user_id, devices):
        self.handlers = {
            actions.ACTION_SYNC: self.handle_sync_request,
            actions.ACTION_QUERY: self.handle_query_request,
            actions.ACTION_EXECUTE: self.handle_execute_request,
            actions.ACTION_DISCONNECT: self.handle_disconnect_request,
        }
        self.agent_user_id = agent_user_id
        self.devices = dict()
        for device in devices:
            self.devices[device.id] = device
        self.current_request_id = None

    def get_device(self, device_id):
        return self.devices.get(device_id)

    def parse_request(self, json_data):
        request_id = json_data.get("requestId")
        if not request_id:
            raise RequestError(None, error.ERROR_PROTOCOL_ERROR)

        inputs = json_data.get("inputs")
        if not inputs:
            raise RequestError(request_id, error.ERROR_PROTOCOL_ERROR)

        return request_id, [(i["intent"], i) for i in inputs]

    def handle_request(self, json_data):
        self.current_request_id, inputs = self.parse_request(json_data)
        for intent, input_ in inputs:
            handler_fn = self.handlers.get(intent)
            if handler_fn:
                return handler_fn(input_)

    def format_sync_response(self):
        return {
            "requestId": self.current_request_id,
            "payload": {
                "agentUserId": self.agent_user_id,
                "devices": list(map(Device.to_json, self.devices)),
            },
        }

    def handle_sync_request(self, input_data):
        return self.format_sync_response()

    def format_query_response(self, devices_status):
        """
        {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "devices": {
                    "123": {
                        "on": true,
                        "online": true
                    },
                    "456": {
                        "on": true,
                        "online": true,
                        "brightness": 80,
                        "color": {
                        "name": "cerulean",
                        "spectrumRGB": 31655
                        }
                    }
                }
            }
        }
        """
        return {
            "requestId": self.current_request_id,
            "payload": {
                "devices": devices_status
            }
        }

    def handle_query_request(self, input_data):
        return self.format_query_response({})

    def handle_execute_request(self, input_data):
        pass

    def handle_disconnect_request(self, input_data):
        pass
