import sqlalchemy as sa
import sqlalchemy.ext.declarative as sa_ext_declarative
import sqlalchemy.orm as sa_orm
import sqlalchemy.schema as sa_schema


_Base = sa_ext_declarative.declarative_base()


class Post(_Base):
  __tablename__ = "Posts"

  id = sa.Column(sa.Integer, primary_key=True)
  creator = sa.Column(sa.String, nullable=False)
  created_datetime = sa.Column(sa.DateTime, nullable=False)
  num_stars = sa.Column(sa.Integer, nullable=False, default=0)
  data = sa.Column(sa.String, nullable=False)


class HashTag(_Base):
  __tablename__ = "HashTags"

  post_id = sa.Column(sa.Integer, sa.ForeignKey("Posts.id"), primary_key=True)
  value = sa.Column(sa.String, primary_key=True)
  created_datetime = sa.Column(sa.DateTime, nullable=False)

  post = sa_orm.relationship("Post", backref=sa_orm.backref("hash_tags"))


class StarredPost(_Base):
  __tablename__ = "StarredPosts"

  post_id = sa.Column(sa.Integer, sa.ForeignKey("Posts.id"), primary_key=True)
  user_id = sa.Column(sa.String, primary_key=True)
  starred_datetime = sa.Column(sa.DateTime, nullable=False)

  post = sa_orm.relationship("Post", backref=sa_orm.backref("stars"))


def _create_table_aliases():
  """Creates an alias for each table, for convenience."""
  global Posts
  global HashTags
  global StarredPosts
  Posts = Post.__table__
  HashTags = HashTag.__table__
  StarredPosts = StarredPost.__table__

_create_table_aliases()


def _define_indexes():
  """Defines the indexes needed for efficient queries."""
  # Return all posts sorted by time.
  sa_schema.Index("PostsByTime", Post.created_datetime, Post.id)
  # Return all posts sorted by time for a given hash tag.
  sa_schema.Index("HashTagsByTime", HashTag.value, HashTag.created_datetime, HashTag.post_id)

_define_indexes()


def create_all_tables(engine):
  """Creates all tables and indexes in the database."""
  _Base.metadata.create_all(engine)


def drop_all_tables(engine):
  """Drops all tables and indexes in the database."""
  _Base.metadata.drop_all(engine)

