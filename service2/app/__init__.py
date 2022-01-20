import logging
import logging.config
from . import contextvars

logging.basicConfig(level=logging.INFO)

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": "%(levelname)s %(name)s %(lineno)d %(message)s",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            }
        },
        "handlers": {"json": {"class": "logging.StreamHandler", "formatter": "json"}},
        "loggers": {"": {"handlers": ["json"], "propagate": False}},
    }
)

old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.request_id = contextvars.REQUEST_ID.get()
    return record


logging.setLogRecordFactory(record_factory)
