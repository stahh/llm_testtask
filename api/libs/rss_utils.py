import logging

import feedparser

logger = logging.getLogger(__name__)


async def parse_feed(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        return feed.entries[:10] if feed.entries else []
    except Exception as e:
        logger.error(f"Error parsing feed: {e}")
        return []
