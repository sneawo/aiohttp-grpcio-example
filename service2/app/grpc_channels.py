import grpc
from typing import AsyncGenerator
import aiohttp
from .grpc.interceptors import RequestIdInterceptor
from .grpc import service1_pb2_grpc


async def grpc_channels_ctx(app: aiohttp.web.Application) -> AsyncGenerator:
    grpc_channel_service1 = grpc.aio.insecure_channel(
        app["config"].SERVICE1_CHANNEL, interceptors=(RequestIdInterceptor(),)
    )
    app["service1_stub"] = service1_pb2_grpc.Service1Stub(grpc_channel_service1)
    yield
    await grpc_channel_service1.close()
