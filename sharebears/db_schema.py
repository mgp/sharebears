import sqlalchemy as sa
import sqlalchemy.ext.declarative as sa_ext_declarative


_Base = sa_ext_declarative.declarative_base()

class User(_Base):
  __tablename__ = "Users"

  id = sa.Column(sa.Integer, primary_key=True)


class Post(_Base):
  __tablename__ = "Posts"

  id = sa.Column(sa.Integer, primary_key=True)
  creator = sa.column(sa.Integer, sa.ForeignKey("User.id"))
  created_time = sa.Column(sa.DateTime, nullable=False)
  num_stars = sa.column(sa.Integer, nullable=False)
  data = sa.column(sa.String, nullable=False)


class HashTag(_Base):
  __tablename__ = "HashTags"

  post_id = sa.Column(sa.Integer, sa.ForeignKey("Post.id"), primary_key=True)
  value = sa.Column(sa.String, primary_key=True)
  created_time = sa.Column(sa.DateTime, nullable=False)


class StarredPost(_Base):
  __tablename__ = "StarredPosts"

  post_id = sa.Column(sa.Integer, sa.ForeignKey("Post.id"), primary_key=True)
  user_id = sa.Column(sa.Integer, sa.ForeignKey("User.id"), primary_key=True)
  created_time = sa.Column(sa.DateTime, nullable=False)
  starred_time = sa.Column(sa.DateTime, nullable=False)


def _define_indexes():
  """Defines the indexes needed for efficient queries.
  """
  # Return all posts sorted by time.
  sa_schema.Index("PostsByTime", Post.created_time, Post.id)
  # Return all posts sorted by time for a given hash tag.
  sa_schema.Index("HashTagsByTime", HashTag.value, HashTag.created_time, HashTag.post_id)
  # Return all users that starred a post.
  sa_schema.Index("StarredPostsByUser", StarredPost.user_id, StarredPost.created_time, StarredPost.post_id)

def create_all_tables():
  _define_indexes()

  """Creates all tables and indexes in the database."""
  _Base.metadata.create_all(_engine)

def drop_all_tables():
  """Drops all tables and indexes in the database."""
  _Base.metadata.drop_all(_engine)

