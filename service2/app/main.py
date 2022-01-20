import logging
import sys
from aiohttp import web

from . import grpc_channels, middlewares
from .views import routes
from .config import Config

logger = logging.getLogger("main")


def init(config: Config) -> web.Application:
    logger.info(f"action=init_app, {config}")
    app = web.Application(middlewares=[middlewares.error_middleware, middlewares.request_id_middleware])
    app["config"] = config

    app.add_routes(routes)

    app.cleanup_ctx.append(grpc_channels.grpc_channels_ctx)

    return app


if __name__ == "__main__":
    access_log_format = "request: %a %r %s %b %Tf %s %b"
    config = Config()
    app = init(config)
    try:
        web.run_app(app, port=config.PORT, access_log_format=access_log_format, print=lambda *args: None)
    except Exception:
        logger.exception("action=run_app, status=failed")
        sys.exit(1)
