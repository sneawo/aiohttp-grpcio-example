import logging
import aiohttp
from .grpc import service1_pb2, service1_pb2_grpc


logger = logging.getLogger(__name__)


async def say_hello(*, app: aiohttp.web.Application, name: str) -> str:
    name_response = await app["service1_stub"].ProcessName(service1_pb2.ProcessNameRequest(name=name), timeout=10)
    hello = f"Hello, {name_response.name}!"
    logger.info(f"action=say_hello, status=success, hello={hello}")
    return hello
