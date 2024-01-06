from marshmallow import ValidationError

from wewu_less.logging import WeWuLogger

logger = WeWuLogger()


def wewu_cloud_function(fn):
    def wewu_cloud_function_wrapper(*args, **kwargs):
        logger.info("Starting function execution", function_name=fn.__name__)
        try:
            result = fn(*args, **kwargs)
            logger.info("Function executed successfully", function_name=fn.__name__)
            return result
        except ValidationError as ve:
            logger.exception(
                "Function executed with validation error", function_name=fn.__name__
            )
            return ve.messages_dict, 400
        except Exception as e:
            logger.exception("Function executed with error", function_name=fn.__name__)
            return str(e), 500

    return wewu_cloud_function_wrapper
