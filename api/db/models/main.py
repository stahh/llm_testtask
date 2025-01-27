from db.database import Base
from sqlalchemy import ARRAY, Column, DateTime, Integer, MetaData, String, Text

convention = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_uq",
    "ck": "%(table_name)s_%(constraint_name)s_sk",
    "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fk",
    "pk": "%(table_name)s_pk",
}
metadata_obj = MetaData(naming_convention=convention)


class BaseSQL:

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self) -> str:
        return str(self.as_dict())


# Models
class Article(Base, BaseSQL):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    feed_url = Column(String, index=True)
    description = Column(Text)
    content = Column(Text)
    published_at = Column(DateTime(timezone=True))


class UserPreferences(Base, BaseSQL):
    __tablename__ = "user_preferences"

    user_id = Column(Integer, primary_key=True, index=True)
    topics = Column(String)
    prev_queries = Column(ARRAY(String))
