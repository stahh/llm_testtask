import logging
from typing import Any

from fastapi import APIRouter, Depends
from libs.llm import embeddings, summarization_chain, vector_store
from service import schemas, llm

logger = logging.getLogger(__name__)

nn_route = APIRouter()


@nn_route.post("/recommendations")
async def get_recommendations(
    preferences: schemas.UserPreferences,
    vector=Depends(vector_store),
    llm_chain=Depends(summarization_chain),
    embeddings_model=Depends(embeddings),
) -> dict[str, Any]:
    query = " ".join(preferences.topics)
    return {
        "result": await service.get_recommendation(
            query, vector, llm_chain, embeddings_model
        )
    }


@nn_route.post("/assistant")
async def agent_query(
    query: schemas.AgentQuery,
    vector=Depends(vector_store),
    llm_chain=Depends(summarization_chain),
    embeddings_model=Depends(embeddings),
) -> dict[str, Any]:
    return {
        "result": await service.get_recommendation(
            query.question, vector, llm_chain, embeddings_model
        )
    }
