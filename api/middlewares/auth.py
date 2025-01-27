import json
import logging

from fastapi import Request, Response
from service.schemas import User, UserRole
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)


async def get_authenticated_user(token: str) -> User:
    return User(
        id=1,
        token=token,
        role=UserRole.ADMIN,
    )


class UserAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if not request.url.path.startswith("/v1"):
            return await call_next(request)
        if not (token := request.headers.get("Authorization")):
            logger.error(
                "Unauthorized",
                extra={
                    "error_status_code": 401,
                },
            )
            return Response(
                content=json.dumps({"detail": "Unauthorized"}),
                status_code=401,
                media_type="application/json",
            )

        if not (user := await get_authenticated_user(token)):
            logger.error(
                "User Not Found",
                extra={
                    "error_status_code": 404,
                    "token": token,
                },
            )
            return Response(
                content=json.dumps({"detail": "Not Found"}),
                status_code=404,
                media_type="application/json",
            )
        request.scope["user"] = user
        response = await call_next(request)
        return response
