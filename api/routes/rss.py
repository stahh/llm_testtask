import asyncio
import logging

import aiohttp
from conf import FEEDS, NN_HOST
from db.database import database
from fastapi import APIRouter, Depends
from libs.llm import vector_store, embeddings
from routes.headers import token_header
from service import schemas, llm
from starlette.requests import Request

logger = logging.getLogger(__name__)

rss_router = APIRouter(
    prefix="/v1/rss",
    dependencies=[
        Depends(token_header),
    ],
)


# API endpoints
@rss_router.get("/refresh")
async def refresh_rss(
    db_session=Depends(database.get_session),
    vector=Depends(vector_store),
embeddings_model=Depends(embeddings),
) -> dict[str, str]:
    tasks = [
        llm.parse_and_store_rss(feed_url, db_session, vector, embeddings_model) for feed_url in FEEDS
    ]
    await asyncio.gather(*tasks)
    return {"message": "RSS feeds refreshed."}


@rss_router.get("/users/recommendations")
async def get_recommendations(
    request: Request,
    db_session=Depends(database.get_session),
) -> list[schemas.Topic | None]:
    user = request.scope["user"]
    preferences = await llm.get_user_preference(user.id, db_session)
    if not preferences:
        # Some random recommendations?
        return []
    async with aiohttp.ClientSession() as session:
        result = await session.post(
            f"{NN_HOST}/recommendations", json=preferences.model_dump(mode="json")
        )
        if result.status != 200:
            return []
        result = await result.json()
        return result.get("result")


@rss_router.post("/users/preferences")
async def add_preferences(
    request: Request,
    topics: list[str],
    db_session=Depends(database.get_session),
) -> dict[str, str]:
    user = request.scope["user"]
    await llm.add_user_preference(user.id, topics, db_session)
    return {"message": f"Topics {topics} added"}


@rss_router.post("/assistant/query")
async def agent_query(
    query: schemas.AgentQuery,
    db_session=Depends(database.get_session),
    vector=Depends(vector_store),
embeddings_model=Depends(embeddings),
) -> list[schemas.Topic | None]:

    search_results = await llm.get_recommendation_by_topic(db_session)
    tasks = [
        llm.parse_and_store_rss(result, database.get_session(), vector, embeddings_model)
        for result in search_results
    ]
    _ = await asyncio.gather(*tasks)

    async with aiohttp.ClientSession() as session:
        result = await session.post(
            f"{NN_HOST}/assistant",
            json=query.model_dump(mode="json"),
            headers={"Content-Type": "application/json"},
        )
        result = await result.json()
        return result.get("result")
