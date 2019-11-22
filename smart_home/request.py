from . import error
from . import actions
from . import Device
from . import auth

import logging


class RequestHandler(object):
    def __init__(self, agent_user_id, devices, key_path="/usr/src/app/key.json"):
        self.logger = logging.getLogger("RequestHandler")
        self.handlers = {
            actions.ACTION_SYNC: self.handle_sync_request,
            actions.ACTION_QUERY: self.handle_query_request,
            actions.ACTION_EXECUTE: self.handle_execute_request,
            actions.ACTION_DISCONNECT: self.handle_disconnect_request,
        }
        self.agent_user_id = agent_user_id
        self.devices = dict()
        for device in devices:
            self.logger.debug("Adding device with id %s", device.id)
            self.devices[device.id] = device
        self.current_request_id = None

        credentials = auth.create_credentials(key_path)
        self.authorized_session = auth.create_authorized_session(credentials)
        self.report_state_url = (
            "https://homegraph.googleapis.com/v1/devices:reportStateAndNotification"
        )

    def get_device(self, device_id):
        return self.devices.get(device_id)

    def parse_request(self, json_data):
        request_id = json_data.get("requestId")
        if not request_id:
            raise error.RequestError(None, error.ERROR_PROTOCOL_ERROR)

        inputs = json_data.get("inputs")
        if not inputs:
            raise error.RequestError(request_id, error.ERROR_PROTOCOL_ERROR)

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
                "devices": list(map(Device.to_json, self.devices.values())),
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
            "payload": {"devices": devices_status},
        }

    def handle_query_request(self, input_data):
        return self.format_query_response({})

    def format_execute_response(self, commands):
        """
        {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "commands": [
                    {
                        "ids": [
                            "123"
                        ],
                        "status": "SUCCESS",
                        "states": {
                            "on": true,
                            "online": true
                        }
                    },
                    {
                        "ids": [
                            "456"
                        ],
                        "status": "ERROR",
                        "errorCode": "deviceTurnedOff"
                    }
                ]
            }
        }
        """
        return {"requestId": self.current_request_id, "payload": {"commands": commands}}

    def handle_execute_request(self, input_data):
        pass

    def handle_disconnect_request(self, input_data):
        pass

    def report_state(self, state):
        self.authorized_session.post(url=self.report_state_url, json=state)
