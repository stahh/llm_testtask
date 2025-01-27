import datetime
from time import mktime

from chromadb.api.models import Collection
from db import models
from libs.rss_utils import parse_feed
from service import schemas
from sqlalchemy import distinct, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


async def parse_and_store_rss(
    feed_url: str, db_session: AsyncSession, vector: Collection
) -> None:
    feed = await parse_feed(feed_url)
    if not feed:
        return
    documents = []
    ids = []
    metadatas = []
    async with db_session as sess:
        for entry in feed:
            statement = select(models.Article).where(models.Article.url == entry.link)
            result = await sess.scalar(statement)
            if not result:
                try:
                    dt = datetime.datetime.fromtimestamp(mktime(entry.published_parsed))
                except AttributeError:
                    dt = datetime.datetime.now(tz=datetime.UTC)
                article = models.Article(
                    id=entry.id,
                    title=entry.title,
                    url=entry.link,
                    feed_url=feed_url,
                    description=entry.get("description", ""),
                    content=entry.get("content", [{}])[0].get("value", ""),
                    published_at=dt,
                )
                sess.add(article)
                doc = (
                    entry.get("content", [{}])[0].get("value", "")
                    or entry.get("description", "")
                    or entry.title
                )
                documents.append(doc)
                metadatas.append(
                    {
                        "title": article.title,
                        "url": article.url,
                        "feed_url": feed_url,
                        "published_at": article.published_at.timestamp(),
                    }
                )
                ids.append(article.id)
        await sess.commit()
    if ids and documents and metadatas:
        vector.add(documents=documents, metadatas=metadatas, ids=ids)


async def get_user_preference(
    user_id: str, db_session: AsyncSession
) -> schemas.UserPreferences | None:
    statement = select(models.UserPreferences).where(
        models.UserPreferences.user_id == user_id
    )
    async with db_session as sess:
        result = await sess.scalar(statement)
        if not result:
            return None
        return schemas.UserPreferences.model_validate(result.as_dict())


async def get_recommendation_by_topic(
    db_session: AsyncSession,
) -> list[str]:
    dt = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=7)
    async with db_session as sess:
        statement = select(distinct(models.Article.feed_url)).where(
            models.Article.published_at < dt
        )
        search_results = await sess.scalars(statement)
    return [x for x in search_results]


async def add_user_preference(
    user_id: int, topics: list[str], db_session: AsyncSession
) -> None:
    insert_statement = (
        insert(models.UserPreferences)
        .values(user_id=user_id, topics=",".join(topics))
        .returning(models.UserPreferences)
    )
    async with db_session as session:
        await session.scalar(insert_statement)
        await session.commit()
