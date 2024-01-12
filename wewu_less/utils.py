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


def wewu_json_http_cloud_function(fn, accepts_body=True):
    def wewu_json_http_cloud_function_wrapper(request: flask.Request, *args, **kwargs):
        content_header = request.headers["content-type"]

        if content_header != "application/json":
            return NON_JSON_ERROR

        try:
            if accepts_body:
                request_json: dict = request.get_json(silent=True)
                if not request_json:
                    return "Invalid body, it needs to be valid JSON", 400

                response = fn(request_json)
            else:
                response = fn()
        except ValidationError as ve:
            return ve.messages_dict, 400
        except Exception:
            logger.exception(
                "Uncaught exception in handler",
            )
            return {}, 500

        if response is None:
            response = {}, 200
        elif isinstance(response, dict):
            response = response, 200

        return response

    return wewu_cloud_function(wewu_json_http_cloud_function_wrapper)


def wewu_event_cloud_function(fn):
    def wewu_event_cloud_function_wrapper(event, *args, **kwargs):
        return fn(event)

    return functions_framework.cloud_event(
        wewu_cloud_function(wewu_event_cloud_function_wrapper)
    )
