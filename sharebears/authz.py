import flask
import functools


def _get_client_values(client):
  """Assigns values from the session to the request globals"""

  flask.g.logged_in = True
  flask.g.email_address = client['email_address']
  flask.g.name = client['name']
  flask.g.client_auth = client['auth']


def login_required(f):
  """Decorates the given function so that login is required.
  
  If the client is logged in, session values are available as request
  globals.
  """

  page_name = f.__name__

  @functools.wraps(f)
  def decorated_function(*pargs, **kwargs):
    client = flask.session.get('client', None)
    if client is None:
      flask.abort(requests.codes.unauthorized)

    _get_client_values(client)
    flask.g.page_name = page_name
    return f(*pargs, **kwargs)

  return decorated_function


def login_optional(f):
  """Decorates the given function so that login is optional.

  If the client is logged in, session values are available as request
  globals.
  """

  page_name = f.__name__

  @functools.wraps(f)
  def decorated_function(*pargs, **kwargs):
    client = flask.session.get('client', None)
    if client:
      _get_client_values(client)
    else:
      flask.g.logged_in = False
      flask.g.email_address = None
      flask.g.name = None
      flask.g.client_auth = None

    flask.g.page_name = page_name
    return f(*pargs, **kwargs)

  return decorated_function
