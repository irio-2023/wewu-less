import os

import structlog
from marshmallow import ValidationError

from wewu_less.logging import get_logger

logger = get_logger()


def wewu_cloud_function(fn):
    def wewu_cloud_function_wrapper(*args, **kwargs):
        structlog.contextvars.clear_contextvars()
        lambda_identifier = os.getenv("LAMBDA_IDENTIFIER", None)
        structlog.contextvars.bind_contextvars(function_name=lambda_identifier)
        try:
            result = fn(*args, **kwargs)
            return result
        except ValidationError as ve:
            return ve.messages_dict, 400
        except Exception as e:
            return str(e), 500

    return wewu_cloud_function_wrapper
