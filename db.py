from db_schema import User, Post, HashTag, StarredPost
from db_util import close_session, DbException, optional_one

from datetime import datetime
import sqlalchemy.ext.declarative as sa_ext_declarative


def _utcnow(now):
  """Returns the given time if not None, or datetime.utcnow() otherwise.
  """
  if now is None:
    return datetime.utcnow()
  return now


@db_util.close_session
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


@db_util.close_session
def get_post(post_id):
  now = _utcnow(now)

  # TODO


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


@db_util.close_session
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


@close_session
def get_all_posts():
  now = _utcnow(now)


@close_session
def get_posts_for_user(client_id):
  now = _utcnow(now)


@close_session
def get_post_for_hashtag(hash_tag):
  now = _utcnow(now)

