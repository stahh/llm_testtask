import logging

from libs.rss_utils import parse_feed
from service import schemas
from db.dao import sql, vector

logger = logging.getLogger(__name__)


async def parse_and_store_rss(
    feed_url: str,
) -> None:
    feed = await parse_feed(feed_url)
    if not feed:
        return
    embeddings = []
    documents = []
    ids = []
    metadatas = []
    for entry in feed:
        try:
            documents, embeddings, metadatas, ids = await sql.add_entry(entry, feed_url)
        except Exception as e:
            logger.error(f"Error adding entry: {e}")

    if ids:
        try:
            await vector.add_docs(documents=documents,
                            embeddings=embeddings,
                            metadatas=metadatas,
                            ids=ids)
        except Exception as e:
            logger.error(f"Error adding docs to vector: {e}")


async def get_user_preference(
    user_id: str
) -> schemas.UserPreferences | None:
    try:
        return await sql.get_user_preference(user_id)
    except Exception as e:
        logger.error(f"Error getting user preference: {e}")
        return None


async def get_recommendation_by_topic() -> list[str]:
    try:
        return await sql.get_last_rss_entries()
    except Exception as e:
        logger.error(f"Error getting last rss entries: {e}")
        return []


async def add_user_preference(
    user_id: int,
    topics: list[str],
) -> None:
    try:
        return await sql.add_user_preference(user_id, topics)
    except Exception as e:
        logger.error(f"Error adding user preference: {e}")
        return None
