import base64
import json
import os

import flask
import functions_framework
import structlog
from marshmallow import ValidationError

from wewu_less.logging import get_logger

logger = get_logger()

NON_JSON_ERROR = {"error": "Body must be JSON string"}, 400


def wewu_cloud_function(fn):
    def wewu_cloud_function_wrapper(*args, **kwargs):
        structlog.contextvars.clear_contextvars()
        lambda_identifier = os.getenv("LAMBDA_IDENTIFIER", None)
        structlog.contextvars.bind_contextvars(function_name=lambda_identifier)
        return fn(*args, **kwargs)

    return wewu_cloud_function_wrapper


def wewu_json_http_cloud_function(*args, accepts_body=True, accepts_params=False):
    return lambda x: _wewu_json_http_cloud_function(
        x, accepts_body=accepts_body, accepts_params=accepts_params
    )


def _wewu_json_http_cloud_function(fn, accepts_body, accepts_params):
    def wewu_json_http_cloud_function_wrapper(request: flask.Request, *args, **kwargs):
        function_args_list = []

        if accepts_body:
            content_header = request.headers["content-type"]
            if content_header != "application/json":
                return NON_JSON_ERROR
            request_json: dict = request.get_json(silent=True)
            if not request_json:
                return "Invalid body, it needs to be valid JSON", 400
            function_args_list.append(request_json)

        if accepts_params:
            function_args_list.append(request.args.to_dict(flat=True))

        try:
            function_args = tuple(function_args_list)
            response = fn(*function_args)
        except ValidationError as ve:
            logger.exception("Failed to validate request in the cloud function")
            return ve.messages_dict, 400
        except Exception:
            logger.exception(
                "Uncaught exception in handler",
            )
            return {
                "error": None,
                "message": "Server could not process the request because of "
                "internal error. Please try again later of contact support "
                "if that error persists.",
            }, 500

        if response is None:
            response = {}, 200
        elif isinstance(response, dict):
            response = response, 200

        return response

    return wewu_cloud_function(wewu_json_http_cloud_function_wrapper)


def wewu_event_cloud_function(fn):
    def wewu_event_cloud_function_wrapper(base64_event, *args, **kwargs):
        try:
            event = json.loads(base64.b64decode(base64_event["data"]))
        except ValidationError:
            logger.exception(
                "Failed to validate event in the cloud function", _event=base64_event
            )
            return
        except Exception:
            logger.exception(
                "Failed to deserialize event in event-driven Cloud Function",
                _event=base64_event,
            )
            return
        return fn(event)

    return functions_framework.cloud_event(
        wewu_cloud_function(wewu_event_cloud_function_wrapper)
    )
