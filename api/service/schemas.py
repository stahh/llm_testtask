from enum import Enum

from pydantic import BaseModel


class UserRole(Enum):
    USER = 1
    ADMIN = 2
    ROOT = 3


class User(BaseModel):
    id: int
    token: str
    role: UserRole = UserRole.USER


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
