from aiohttp import web
from . import services

routes = web.RouteTableDef()


@routes.get("/api/v1/say-hello")
async def say_hello(request: web.Request) -> web.Response:
    name = request.query.get("name", "")
    hello = await services.say_hello(app=request.app, name=name)
    return web.json_response(hello)
