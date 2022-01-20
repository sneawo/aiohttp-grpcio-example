from uuid import uuid4
from typing import Callable
from aiohttp import web
from . import contextvars


@web.middleware
async def error_middleware(request: web.Request, handler: Callable) -> web.Response:
    try:
        response = await handler(request)
        return response
    except (web.HTTPBadRequest, web.HTTPRedirection):
        raise
    except web.HTTPException as ex:
        return web.json_response({"error": ex.reason}, status=ex.status)
    except Exception as ex:
        if request.app["config"].DEBUG:
            raise
        return web.json_response({"error": str(ex)}, status=500)


@web.middleware
async def request_id_middleware(request: web.Request, handler: Callable) -> web.Response:
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    contextvars.REQUEST_ID.set(request_id)
    response = await handler(request)
    response.headers["X-Request-ID"] = request_id
    return response
