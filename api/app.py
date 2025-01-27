import logging
from contextlib import asynccontextmanager

from db.database import database, setup_database
from fastapi import FastAPI
from middlewares.auth import UserAuthMiddleware
from routes.rss import rss_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await setup_database()
    yield
    await database.close_database()


logger = logging.getLogger(__name__)


def init_app() -> FastAPI:

    app = FastAPI(
        lifespan=lifespan,  # type: ignore
        title="RSS Feeds",
    )
    app.include_router(rss_router)
    app.add_middleware(UserAuthMiddleware)  # type: ignore
    return app


app = init_app()
