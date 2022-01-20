from aiohttp import web
from . import services

routes = web.RouteTableDef()


@routes.get("/api/v1/name")
async def process_name(request: web.Request) -> web.Response:
    name = request.query.get("name", "")
    name = await services.process_name(name=name)
    return web.json_response({"name": name})
