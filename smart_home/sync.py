from smart_home import error
from smart_home import actions
from smart_home.device import Device


def handle_sync_request(json_data, agent_user_id, devices):
    request_id = json_data.get("requestId")
    if not request_id:
        return error.format_error(None, error.ERROR_PROTOCOL_ERROR)

    inputs = json_data.get("inputs")
    if not inputs:
        return error.format_error(request_id, error.ERROR_PROTOCOL_ERROR)

    intent = inputs[0].get("intent")
    if not intent:
        return error.format_error(request_id, error.ERROR_PROTOCOL_ERROR)

    if intent != actions.ACTION_SYNC:
        return error.format_error(request_id, error.ERROR_NOT_SUPPORTED)

    return {
        "requestId": request_id,
        "payload": {
            "agentUserId": agent_user_id,
            "devices": list(map(Device.to_json, devices)),
        },
    }
