import json
from unittest.mock import MagicMock

import flask
from cloudevents.http import CloudEvent


def make_request_from_json_str(body: str) -> flask.Request:
    request_mock = MagicMock()

    def get_json_mock(*args, **kwargs) -> dict:
        return json.loads(body)

    request_mock.get_json = get_json_mock
    request_mock.headers = {"content-type": "application/json"}

    return request_mock


def make_event_from_str(body: str) -> CloudEvent:
    event_mock = MagicMock()
    get_data_mock = MagicMock(return_value=body)

    event_mock.get_data = get_data_mock
    return event_mock
