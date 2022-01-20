from contextvars import ContextVar

REQUEST_ID = ContextVar("request_id", default="")
