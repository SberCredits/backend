import datetime
from typing import Callable

from fastapi import HTTPException
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST

from dependencies.queues import audit

"""
    type: Mapped[str] = mapped_column(String)
    detail: Mapped[str] = mapped_column(String, nullable=True)
    application: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    ip_address: Mapped[str] = mapped_column(String)
"""


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            ip_address = request.headers.get("X-LOCATION")
            if not ip_address:
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="X-LOCATION Header is required!")

            response: Response = await original_route_handler(request)

            audit.log(
                type=response.status_code,
                detail=f"{request.url} {response.body}",
                created_at=datetime.datetime.now(),
                ip_address=ip_address
            )
            return response

        return custom_route_handler
