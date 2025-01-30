import logging
from typing import Any

from fastapi import APIRouter
from service import schemas, recommendation

logger = logging.getLogger(__name__)

nn_route = APIRouter()


@nn_route.post("/recommendations")
async def get_recommendations(
    preferences: schemas.UserPreferences,
) -> dict[str, Any]:
    query = " ".join(preferences.topics)
    return {
        "result": await recommendation.get_recommendation(
            query
        )
    }


@nn_route.post("/assistant")
async def agent_query(
    query: schemas.AgentQuery,
) -> dict[str, Any]:
    return {
        "result": await recommendation.get_recommendation(
            query.question
        )
    }
