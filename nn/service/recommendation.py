from service import schemas
from libs.llm import embeddings as embedding_model
from libs.llm import summarization_chain as llm_chain
from libs.llm import vector_store as vector


async def get_recommendation(
    query: str
) -> list[schemas.Topic | None]:
    query_embedding = embedding_model.embed_query(query)
    search_results = vector.query(query_embeddings=query_embedding, n_results=5)
    recommendations = []
    for metadata in search_results.get("metadatas", []):
        if metadata:
            summary = llm_chain.run(article=metadata[0]["title"])
            recommendations.append(
                schemas.Topic.model_validate(
                    **{
                        "title": metadata[0]["title"],
                        "url": metadata[0]["url"],
                        "summary": summary,
                        "feed_url": metadata[0]["feed_url"],
                    }
                )
            )
    return recommendations
