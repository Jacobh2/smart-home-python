ERROR_AUTH_EXPIRED = "authExpired"
ERROR_AUTH_FAILURE = "authFailure"
ERROR_DEVICE_OFFLINE = "deviceOffline"
ERROR_TIMEOUT = "timeout"
ERROR_DEVICE_TURNED_OFF = "deviceTurnedOff"
ERROR_DEVICE_NOT_FOUND = "deviceNotFound"
ERROR_VALUE_OUT_OF_RANGE = "valueOutOfRange"
ERROR_NOT_SUPPORTED = "notSupported"
ERROR_PROTOCOL_ERROR = "protocolError"
ERROR_UNKNOWN_ERROR = "unknownError"

ERROR_CODES = [
    ERROR_AUTH_EXPIRED,
    ERROR_AUTH_FAILURE,
    ERROR_DEVICE_OFFLINE,
    ERROR_TIMEOUT,
    ERROR_DEVICE_TURNED_OFF,
    ERROR_DEVICE_NOT_FOUND,
    ERROR_VALUE_OUT_OF_RANGE,
    ERROR_NOT_SUPPORTED,
    ERROR_PROTOCOL_ERROR,
    ERROR_UNKNOWN_ERROR,
]


def format_error(request_id, error_code):
    if error_code not in ERROR_CODES:
        error_code = ERROR_UNKNOWN_ERROR

    return {"requestId": request_id, "payload": {"errorCode": error_code}}
