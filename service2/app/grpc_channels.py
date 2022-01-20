import logging
import grpc
from typing import AsyncGenerator
import aiohttp
from .grpc.interceptors import RequestIdInterceptor

logger = logging.getLogger(__name__)


async def grpc_channels_ctx(app: aiohttp.web.Application) -> AsyncGenerator:
    app["grpc_channel_service1"] = grpc.aio.insecure_channel(
        app["config"].SERVICE1_CHANNEL, interceptors=(RequestIdInterceptor(),)
    )
    yield
    await app["grpc_channel_service1"].close()
