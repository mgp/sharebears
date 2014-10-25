import functools
import sqlalchemy as sa
import sqlalchemy.engine as sa_engine
import sqlalchemy.orm as sa_orm
import sys


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


def optional_one(query):
  """Like calling one() on query, but returns None instead of raising
  NoResultFound.
  """
  results = query.limit(1).all()
  if results:
    return results[0] 
  return None

