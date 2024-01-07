import structlog
import structlog_gcp


def _ensure_structlog_configured():
    if structlog.is_configured():
        return

    processors = [
        structlog.contextvars.merge_contextvars,
        *structlog_gcp.build_processors(),
    ]

    structlog.configure(processors)


def get_logger() -> structlog.stdlib.BoundLogger:
    _ensure_structlog_configured()
    return structlog.get_logger()
