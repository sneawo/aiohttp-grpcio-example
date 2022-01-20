import asyncio
import logging
from typing import AsyncGenerator, Awaitable, Callable

import grpc
from aiohttp import web
from .grpc import service1_pb2, service1_pb2_grpc
from . import contextvars, services


logger = logging.getLogger(__name__)


class RequestIdInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        for (header, value) in handler_call_details.invocation_metadata:
            if header == "request_id":
                contextvars.REQUEST_ID.set(value)
                break
        return await continuation(handler_call_details)


class Service1(service1_pb2_grpc.Service1Servicer):
    def __init__(self, app: web.Application) -> None:
        self.app = app

    async def ProcessName(
        self, request: service1_pb2.ProcessNameRequest, context: grpc.aio.ServicerContext
    ) -> service1_pb2.ProcessNameResponse:
        name = await services.process_name(name=request.name)
        return service1_pb2.ProcessNameResponse(name=name)


def _init(app: web.Application, listen_addr: str) -> grpc.aio.Server:
    server = grpc.aio.server(interceptors=(RequestIdInterceptor(),))
    server.add_insecure_port(listen_addr)
    service1_pb2_grpc.add_Service1Servicer_to_server(Service1(app), server)
    return server


async def _start_grpc_server(server: grpc.aio.Server) -> None:
    await server.start()
    await server.wait_for_termination()


async def grpc_server_ctx(app: web.Application) -> AsyncGenerator:
    listen_addr = "[::]:50051"

    server = _init(app, listen_addr)
    task = asyncio.create_task(_start_grpc_server(server))
    logger.info(f"action=init_grpc_server, address={listen_addr}")

    yield

    await server.stop(grace=None)
    task.cancel()
    await task
