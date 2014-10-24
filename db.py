from datetime import datetime
import functools
import sqlalchemy as sa
import sqlalchemy.engine as sa_engine
import sqlalchemy.ext.declarative as sa_ext_declarative
import sqlalchemy.orm as sa_orm
import sys


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


def define_indexes():
  """Defines the indexes needed for efficient queries.
  """
  # Return all posts sorted by time.
  sa_schema.Index("PostsByTime", Post.created_time, Post.id)
  # Return all posts sorted by time for a given hash tag.
  sa_schema.Index("HashTagsByTime", HashTag.value, HashTag.created_time, HashTag.post_id)
  # Return all users that starred a post.
  sa_schema.Index("StarredPostsByUser", StarredPost.user_id, StarredPost.created_time, StarredPost.post_id)

def create_all_tables():
  define_indexes()

  """Creates all tables and indexes in the database."""
  _Base.metadata.create_all(_engine)

def drop_all_tables():
  """Drops all tables and indexes in the database."""
  _Base.metadata.drop_all(_engine)


# TODO(mgp): Make this not global?
_engine = None
session = None
def create_session(database, database_uri):
  if database == 'sqlite':
    # http://docs.sqlalchemy.org/en/rel_0_9/dialects/sqlite.html#foreign-key-support
    @sa.event.listens_for(sa_engine.Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
      cursor = dbapi_connection.cursor()
      cursor.execute("PRAGMA foreign_keys=ON")
      cursor.close()

  global _engine
  _engine = sa.create_engine(database_uri, convert_unicode=True, echo=False)

  # Use scoped_session with Flask: http://flask.pocoo.org/docs/patterns/sqlalchemy/
  global session
  session = sa_orm.scoped_session(sa_orm.sessionmaker(
      autocommit=False, autoflush=False, bind=_engine))

  # Create aliases for each table.
  global Users
  global Posts
  global HashTags
  global StarredPosts
  Users = User.__table__
  Posts = Post.__table__
  HashTags = HashTag.__table__
  StarredPosts = StarredPost.__table__


def close_session(f):
  """A decorator that closes the session before returning a result.
  """

  @functools.wraps(f)
  def decorated_function(*pargs, **kwargs):
    result = f(*pargs, **kwargs)
    session.close()
    return result
  return decorated_function


class DbException(Exception):
  """Exception class raised by the database.
  """

  def __init__(self, reason):
    Exception.__init__(self)
    self.reason = reason

  def __str__(self):
    return str(self.reason)

  @staticmethod
  def _chain():
    exception_type, exception_value, traceback = sys.exc_info()
    raise DbException(exception_value), None, traceback


def _utcnow(now):
  """Returns the given time if not None, or datetime.utcnow() otherwise.
  """
  if now is None:
    return datetime.utcnow()
  return now


def optional_one(query):
  """Like calling one() on query, but returns None instead of raising
  NoResultFound.
  """
  results = query.limit(1).all()
  if results:
    return results[0] 
  return None


@close_session
def add_post(user_id, data, hash_tags, now=None):
  now = _utcnow(now)

  try:
    # Add the post.
    post = Post(creator=user_id, created_time=now, data=data)
    session.add(post)
    session.flush()
    post_id = post.id

    # Add its hash tags.
    for hash_tag_value in hash_tags:
      hash_tag = HashTag(post_id=post_id, value=hash_tag_value, created_time=now)
      session.add(hash_tag)
    session.commit()

    return post_id
  except sa.exc.IntegrityError:
    session.rollback()
    raise common_db.DbException._chain()


@close_session
def get_post(post_id):
  # TODO
  pass
  

@close_session
def star_post(user_id, post_id, now=None):
  now = _utcnow(now)

  try:
    # Get the time at which the post was created.
    created_time = session.query(Post.created_time)\
        .filter(Post.id == post_id)\
        .one()\
        .created_time
    # Add the user's star for this post.
    starred_post = StarredPost(post_id=post_id,
        user_id=user_id,
        created_time=created_time,
        starred_time=now)
    session.add(starred_post)
    session.flush()
  except sa_orm.exc.NoResultFound:
    session.rollback()
    raise common_db.DbException._chain()
  except sa.exc.IntegrityError:
    # The flush failed because the user has already starred this post.
    session.rollback()
    raise common_db.DbException._chain()
  
  # Increment the count of stars for the post.
  session.execute(Posts.update()
      .where(Post.id == post_id)
      .values({Post.num_stars: Post.num_stars + 1}))

  session.commit()


@close_session
def unstar_post(user_id, post_id, now=None):
  now = _utcnow(now)

  # Remove the user's star for the post.
  result = session.execute(StarredPosts.delete().where(sa.and_(
      StarredPost.user_id == user_id,
      StarredPost.post_id == post_id)))
  if not result.rowcount:
    session.rollback()
    return

  # Decrement the count of stars for the post.
  session.execute(Posts.update()
      .where(Post.id == post_id)
      .values({Post.num_stars: Post.num_stars - 1}))



