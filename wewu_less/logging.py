import sys
import traceback

from google.cloud import logging

logging_client = logging.Client()


class WeWuLogger:
    logger: logging.Logger

    def __init__(self):
        self.logger = logging_client.logger("wewu_less")

    def _prepare_exc_info(self, kwargs: dict[str, any]):
        exc_info = kwargs.get("exc_info", None)
        if exc_info is not None:
            if isinstance(exc_info, Exception):
                kwargs["exc_info"] = traceback.format_exception(exc_info)
            elif isinstance(exc_info, bool) and exc_info:
                kwargs["exc_info"] = traceback.format_exception(sys.exception())

    def _prepare_kwargs(self, message: str, kwargs: dict[str, any]):
        kwargs["message"] = message
        self._prepare_exc_info(kwargs)

        sets_to_convert = [
            (key, list(value))
            for key, value in kwargs.items()
            if isinstance(value, set)
        ]
        for key, new_value in sets_to_convert:
            kwargs[key] = new_value

    def info(self, message: str, **kwargs):
        self._prepare_kwargs(message, kwargs)
        self.logger.log_struct(kwargs, severity="INFO")

    def error(self, message: str, **kwargs):
        self._prepare_kwargs(message, kwargs)
        self.logger.log_struct(kwargs, severity="ERROR")

    def exception(self, message: str, **kwargs):
        kwargs["exc_info"] = True
        self._prepare_kwargs(message, kwargs)
        self.logger.log_struct(kwargs, severity="ERROR")
