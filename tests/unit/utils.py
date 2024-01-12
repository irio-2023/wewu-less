import base64
import json
from unittest.mock import MagicMock

import flask


def make_request_from_json_str(body: str) -> flask.Request:
    request_mock = MagicMock()

    def get_json_mock(*args, **kwargs) -> dict:
        return json.loads(body)

    request_mock.get_json = get_json_mock
    request_mock.headers = {"content-type": "application/json"}

    return request_mock


def make_event_from_json_str(body: str) -> dict:
    base64_body = base64.b64encode(body.encode())
    return {
        "data": base64_body,
        "publish_time": "2024-01-12T16:45:42.316Z",
        "message_id": "10239849218036796",
    }
