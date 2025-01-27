import logging
import os

from fastapi import FastAPI
from huggingface_hub import login
from routes.nn_route import nn_route

access_token_read = os.getenv("HF_TOKEN")
login(token=access_token_read)

logger = logging.getLogger(__name__)


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(nn_route)
    return app


app = init_app()
