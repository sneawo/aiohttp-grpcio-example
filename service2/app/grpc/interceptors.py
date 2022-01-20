from typing import Callable, Union
import uuid
import grpc
from .. import contextvars


class RequestIdInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def add_request_id_to_metadata(self, client_call_details: grpc.aio.ClientCallDetails) -> None:
        if client_call_details.metadata is not None:
            client_call_details.metadata["request_id"] = contextvars.REQUEST_ID.get()

    async def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.aio.ClientCallDetails, grpc.aio._typing.RequestType], grpc.aio.UnaryUnaryCall],
        client_call_details: grpc.aio.ClientCallDetails,
        request: grpc.aio._typing.RequestType,
    ) -> Union[grpc.aio.UnaryUnaryCall, grpc.aio._typing.ResponseType]:
        self.add_request_id_to_metadata(client_call_details)
        return await continuation(client_call_details, request)
