import flask
import requests

from sharebears import app

import authn_google
import authz
import db
from db import PaginatedSequence
import filters
from github_client import GitHubClient
import json
from post_processor import PostProcessor
from renderable_item import RenderablePost
import resource_summary
import requests
from url_decoder_github import GitHubRepositoryUrlDecoder
from url_decoder_image import ImageUrlDecoder
from url_decoder_twitter import TwitterTweetUrlDecoder
from url_decoder_youtube import YouTubeUrlDecoder


filters.add_to_environment(app.jinja_env)


def _get_post_processor():
  """Returns an PostProcessor configured with the default URL decoders."""
  # TODO(mgp): Authenticate with GitHub.
  github_client = GitHubClient(None, None)
  decoders = [
      GitHubRepositoryUrlDecoder(github_client),
      ImageUrlDecoder(),
      TwitterTweetUrlDecoder(),
      YouTubeUrlDecoder()
  ]
  return PostProcessor(decoders)

post_processor = _get_post_processor()


def _get_renderable_post(post):
  """Returns a RenderablePost instance from the given Post."""
  data = json.loads(post.data)
  renderable_items = post_processor.renderable_items(data)
  return RenderablePost(post.id,
      post.creator,
      post.created_datetime,
      renderable_items,
      post.num_stars,
      post.hash_tags)

def _get_renderable_post_sequence(post_sequence):
  """Returns a PaginatedSequence of RenderablePost instances from the given
  paginated sequence of Post instances.
  """
  renderable_posts = [_get_renderable_post(post) for post in post_sequence.items]
  return PaginatedSequence(renderable_posts)


@app.route('/', methods=["GET"])
@authz.login_optional
def posts():
  all_posts = db.get_posts()
  renderable_all_posts = _get_renderable_post_sequence(all_posts)
  summary = resource_summary.summary_for_renderable_post_sequence(renderable_all_posts)
  return flask.render_template("all_posts.html",
      posts=renderable_all_posts, resource_summary=summary)


def _add_post(user_id, text):
  """Adds a post to the database derived from the given text, by the given user.

  This method returns the identifier of the added post.
  """
  processed_post = post_processor.process(text)
  data_string = json.dumps(processed_post.data)
  post_id = db.add_post(user_id, data_string, processed_post.hash_tags)
  return post_id


_POSTS_PATH = "/posts"
@app.route(_POSTS_PATH, methods=["POST"])
@authz.login_required
def add_post():
  request_form = flask.request.form
  user_id = request_form["user_id"]
  text = request_form["text"]

  post_id = _add_post(user_id, text)
  if post_id:
    post_url = flask.url_for("post", post_id=post_id)
    rendered_template = flask.render_template("post_added.html", post_url=post_url)
    # Return status code 201 Created.
    response = flask.make_response(rendered_template, requests.codes.created)
    # Return the URL for the post in the Location header.
    response.headers["Location"] = post_url
    return response 
  else:
    # TODO: What status code?
    pass


_POST_PATH = "%s/<post_id>" % _POSTS_PATH
@app.route(_POST_PATH)
@authz.login_required
def post(post_id):
  post = db.get_post(post_id)
  if not post:
    flask.abort(requests.codes.not_found)

  renderable_post = _get_renderable_post(post)
  summary = resource_summary.summary_for_renderable_post(renderable_post)
  return flask.render_template("post.html", post=renderable_post, resource_summary=summary)


@app.route("%s/stars" % _POST_PATH)
@authz.login_required
def stars(post_id):
  stars = db.get_stars(post_id)
  return flask.jsonify({"stars": stars})


@app.route("%s/star" % _POST_PATH, methods=["POST"])
@authz.login_required
def star(post_id):
  db.star_post(flask.g.user_id, post_id)
  return flask.jsonify()


@app.route("%s/unstar" %  _POST_PATH, methods=["POST"])
@authz.login_required
def unstar(post_id):
  db.unstar_post(flask.g.user_id, post_id)
  return flask.jsonify()


@app.route("/hashtag/<hash_tag>")
@authz.login_required
def posts_with_hashtag(hash_tag):
  hash_tag_posts = db.get_posts_with_hashtag(hash_tag)
  renderable_hash_tag_posts = _get_renderable_post_sequence(hash_tag_posts)
  summary = resource_summary.summary_for_renderable_post_sequence(renderable_hash_tag_posts)
  return flask.render_template("hashtag_posts.html",
      hash_tag=hash_tag, posts=renderable_hash_tag_posts, resource_summary=summary)


@app.route("/user/<user_id>")
@authz.login_required
def posts_by_user(user_id):
  user_posts = db.get_posts_by_user(user_id)
  renderable_user_posts = _get_renderable_post_sequence(user_posts)
  summary = resource_summary.summary_for_renderable_post_sequence(renderable_user_posts)
  return flask.render_template("user_posts.html",
      user_id=user_id, posts=renderable_user_posts, resource_summary=summary)


@app.route("/logout")
def logout():
  # Remove all client data from the session.
  flask.session.pop("client", None)
  # Redirect to the URL that the user came from.
  next_url = flask.request.args.get("next_url")
  if next_url is None:
    next_url = flask.url_for("posts")
  return flask.redirect(next_url)


@app.errorhandler(requests.codes.unauthorized)
def unauthorized(e):
  response = "unauthorized"
  status = requests.codes.unauthorized
  headers = {
    "Content-Type": "text/plain; charset=utf-8",
  }
  return flask.make_response((response, status, headers))


@app.errorhandler(requests.codes.not_found)
def page_not_found(e):
  return flask.render_template("error_404.html"), 404


@app.errorhandler(requests.codes.server_error)
def internal_server_error(e):
  return flask.render_template("error_500.html"), 500


if app.config["DEBUG"]:
  @app.route("/new_post")
  @authz.login_required
  def new_post():
    return flask.render_template("new_post.html", action=flask.url_for("add_post"))

