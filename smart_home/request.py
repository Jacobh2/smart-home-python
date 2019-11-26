from . import error
from . import actions
from . import Device
from . import auth

import logging
from os import path
from uuid import uuid4
from time import sleep
from threading import Thread


class RequestHandler(object):
    def __init__(
        self,
        agent_user_id,
        devices,
        execute_handlers,
        key_path="/usr/src/app/key.json",
        agent_user_is_store_path="/usr/src/app/agent.id",
    ):
        self.logger = logging.getLogger("RequestHandler")
        self.handlers = {
            actions.ACTION_SYNC: self.handle_sync_request,
            actions.ACTION_QUERY: self.handle_query_request,
            actions.ACTION_EXECUTE: self.handle_execute_request,
            actions.ACTION_DISCONNECT: self.handle_disconnect_request,
        }
        self.execute_handlers = execute_handlers
        self.logger.debug("Have execute handlers %s", execute_handlers)
        self.agent_user_is_store_path = agent_user_is_store_path
        self._agent_user_id = agent_user_id
        self.devices = dict()
        for device in devices:
            self.logger.debug("Adding device with id %s", device.id)
            self.devices[device.id] = device
        self.current_request_id = None

        self.logger.debug("Loading credentials from path %s", key_path)
        credentials = auth.create_credentials(key_path)
        self.authorized_session = auth.create_authorized_session(credentials)
        self.report_state_url = (
            "https://homegraph.googleapis.com/v1/devices:reportStateAndNotification"
        )

        self.time_sleep_report_state = 10
        # Start report state thread
        self.report_state_thread = Thread(
            name="ReportState", target=self.report_state_threaded, daemon=True
        )

    def _start_report_state_thread(self):
        if self.agent_user_id is not None and not self.report_state_thread.is_alive():
            self.report_state_thread.start()

    @property
    def agent_user_id(self):
        if self._agent_user_id is None and path.exists(self.agent_user_is_store_path):
            with open(self.agent_user_is_store_path, "r") as f:
                self._agent_user_id = f.read()
            self._start_report_state_thread()
        return self._agent_user_id

    @agent_user_id.setter
    def agent_user_id(self, value):
        with open(self.agent_user_is_store_path, "w") as f:
            f.write(value)
        self._agent_user_id = value
        self._start_report_state_thread()

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
        self.logger.debug("Handling sync request with input data %s", input_data)
        return self.format_sync_response()

    def format_query_response(self, devices_status):
        return {
            "requestId": self.current_request_id,
            "payload": {"devices": devices_status},
        }

    def format_device_state(self, device_ids):
        pass

    def handle_query_request(self, input_data):
        self.logger.debug("Handling query request with input data %s", input_data)
        devices = input_data["payload"]["devices"]
        device_ids = [device["id"] for device in devices]
        device_status = self.format_device_state(device_ids)
        return self.format_query_response(device_status)

    def format_execute_response(self, commands):
        return {"requestId": self.current_request_id, "payload": {"commands": commands}}

    def handle_execute_request(self, input_data):
        self.logger.debug("Handling execute request with input data %s", input_data)
        return_payload = dict()
        for command in input_data["payload"]["commands"]:
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

    def handle_disconnect_request(self, input_data):
        self.logger.debug("Handling disconnect request with input data %s", input_data)
        pass

    def report_state(self, state):
        response = self.authorized_session.post(url=self.report_state_url, json=state)
        try:
            self.logger.debug("Response %s: %s", response, response.json())
        except:
            pass

    def report_state_threaded(self):
        try:
            while True:
                # Gather state
                state = self.format_device_state(self.devices.keys())
                payload = {
                    "requestId": str(uuid4()),
                    "agentUserId": self.agent_user_id,
                    "payload": {"devices": {"states": state}},
                }
                self.logger.debug("About to report payload %s", payload)

                # Report the sate
                self.report_state(payload)

                sleep(self.time_sleep_report_state)
        except Exception:
            self.logger.exception("Crash during report state")
