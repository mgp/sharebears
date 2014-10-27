import flask
import requests

from sharebears import app

import authz

@app.errorhandler(requests.codes.unauthorized)
def unauthorized(e):
  response = 'unauthorized'
  status = requests.codes.unauthorized
  headers = {
    'Content-Type': 'text/plain; charset=utf-8',
  }
  return flask.make_response((response, status, headers))


@app.errorhandler(requests.codes.not_found)
@authz.login_optional
def page_not_found(e):
  return flask.render_template('error_404.html'), 404


@app.errorhandler(requests.codes.server_error)
@authz.login_optional
def internal_server_error(e):
  return flask.render_template('error_500.html'), 500


@app.route('/logout')
def logout():
  # Remove all client data from the session.
  flask.session.pop('client', None)
  # Redirect to the URL that the user came from.
  next_url = flask.request.args.get('next_url')
  if next_url is None:
    next_url = flask.url_for('home')
  return flask.redirect(next_url)

