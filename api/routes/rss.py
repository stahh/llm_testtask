import asyncio
import logging

import aiohttp
from conf import FEEDS, NN_HOST
from fastapi import APIRouter, Depends
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
async def refresh_rss() -> dict[str, str]:
    tasks = [
        llm.parse_and_store_rss(feed_url) for feed_url in FEEDS
    ]
    await asyncio.gather(*tasks)
    return {"message": "RSS feeds refreshed."}


@rss_router.get("/users/recommendations")
async def get_recommendations(
    request: Request,
) -> list[schemas.Topic | None]:
    user = request.scope["user"]
    preferences = await llm.get_user_preference(user.id)
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
) -> dict[str, str]:
    user = request.scope["user"]
    await llm.add_user_preference(user.id, topics)
    return {"message": f"Topics {topics} added"}


@rss_router.post("/assistant/query")
async def agent_query(
    query: schemas.AgentQuery,
) -> list[schemas.Topic | None]:

    search_results = await llm.get_recommendation_by_topic()
    tasks = [
        llm.parse_and_store_rss(result)
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
