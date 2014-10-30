"""
See https://github.com/mitsuhiko/flask-oauth/blob/master/example/google.py
"""

import flask
from flask_oauth import OAuth
import requests

from sharebears import app


_GOOGLE_REDIRECT_URI = "/sign_in_google_complete"

_oauth = OAuth()
_google = _oauth.remote_app("google",
    base_url="https://www.google.com/accounts/",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    request_token_url=None,
    request_token_params={
      "scope": "email",
      "response_type": "code"
    },
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_method="POST",
    access_token_params={"grant_type": "authorization_code"},
    consumer_key=app.config["GOOGLE_CLIENT_ID"],
    consumer_secret=app.config["GOOGLE_CLIENT_SECRET"])


@app.route("/sign_in_google")
def sign_in_google():
  callback=flask.url_for("sign_in_google_complete", _external=True)
  return _google.authorize(callback=callback)


def _get_client_json(access_token):
  headers = { "Authorization": "OAuth %s" % access_token }
  response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
  response_json = response.json()

  domain = response_json.get("hd", None)
  if domain != app.config["GOOGLE_APP_DOMAIN"]:
    # This user is not part of this organization's domain.
    return None

  google_id = response_json["id"]
  displayed_name = response_json["email"]
  client = {
    "auth_method": "google",
    "user_id": "google:%s" % google_id,
    "displayed_name": displayed_name
  }
  return client


@app.route(_GOOGLE_REDIRECT_URI)
@_google.authorized_handler
def sign_in_google_complete(response):
  access_token = response["access_token"]
  client = _get_client_json(access_token)
  if not client:
    flask.abort(requests.codes.unauthorized)

  flask.session["client"] = client
  # Default session lifetime is 31 days.
  flask.session.permanent = True

  # Redirect to the URL that the user came from.
  next_url = flask.session.pop("next_url", None)
  if next_url is None:
    next_url = flask.url_for("posts")
  return flask.redirect(next_url)


