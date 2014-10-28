import flask
import requests

from sharebears import app

import authz
import db


_POSTS_PATH = "/posts"
@app.route(_POSTS_PATH, methods=["GET"])
@authz.login_required
def posts():
  all_posts = db.get_posts()
  return flask.render_template("all_posts.html", all_posts=all_posts)


@app.route(_POSTS_PATH, methods=["POST"])
@authz.login_required
def add_post():
  request_form = flask.request.form
  user_id = request_form["user_id"]
  text = request_form["text"]

  post_id = self._add_post(user_id, text)
  if post_id:
    post_url = flask.url_for("post", post_id=post_id)
    rendered_template = render_template("post_added.html")
    # Return status code 201 Created.
    response = make_response(rendered_template, requests.codes.created)
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
  return flask.render_template("post.html", post=post)


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
  hashtag_posts = db.get_posts_with_hashtag(hash_tag)
  return flask.render_template("hashtag_posts.html", hashtag_posts=hashtag_posts)


@app.route("/user/<user_id>")
@authz.login_required
def posts_by_user(user_id):
  user_posts = db.get_posts_by_user(user_id)
  return flask.render_template("user_posts.html", user_posts=user_posts)


@app.route('/logout')
def logout():
  # Remove all client data from the session.
  flask.session.pop('client', None)
  # Redirect to the URL that the user came from.
  next_url = flask.request.args.get('next_url')
  if next_url is None:
    next_url = flask.url_for('home')
  return flask.redirect(next_url)


@app.errorhandler(requests.codes.unauthorized)
def unauthorized(e):
  response = 'unauthorized'
  status = requests.codes.unauthorized
  headers = {
    'Content-Type': 'text/plain; charset=utf-8',
  }
  return flask.make_response((response, status, headers))


@app.errorhandler(requests.codes.not_found)
def page_not_found(e):
  return flask.render_template('error_404.html'), 404


@app.errorhandler(requests.codes.server_error)
def internal_server_error(e):
  return flask.render_template('error_500.html'), 500

