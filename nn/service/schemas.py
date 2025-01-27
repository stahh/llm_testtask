from pydantic import BaseModel


class UserPreferences(BaseModel):
    user_id: int
    topics: str
    prev_queries: list[str] | None = None


class AgentQuery(BaseModel):
    question: str


class Topic(BaseModel):
    title: str
    url: str
    summary: str
    feed_url: str | None = None
