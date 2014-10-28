from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from db_schema import User as MappedUser, Users, Post as MappedPost, Posts, HashTag as MappedHashTag, HashTags, StarredPost as MappedStarredPost, StarredPosts
import db_util
from db_util import DbException


class Post:
  """A post read from the database."""

  def __init__(self, id, creator, created_datetime, data, num_stars, hash_tags):
    self.id = id
    self.creator = creator
    self.created_datetime = created_datetime
    self.data = data
    self.num_stars = num_stars
    self.hash_tags = hash_tags

  def __repr__(self):
    return "Post(id=%r, creator=%r, created_datetime=%r, data=%r, num_stars=%r, hash_tags=%r)" % (
        self.id,
        self.creator,
        self.created_datetime,
        self.data,
        self.num_stars,
        self.hash_tags)


def _utcnow(now):
  """Returns the given time if not None, or datetime.utcnow() otherwise."""
  if now is None:
    return datetime.utcnow()
  return now


@db_util.use_session
def add_post(session, user_id, data, hash_tags, now=None):
  now = _utcnow(now)

  try:
    # Add the post.
    mapped_post = MappedPost(creator=user_id, created_datetime=now, data=data)
    session.add(mapped_post)
    session.flush()
    post_id = mapped_post.id

    # Add its hash tags.
    for hash_tag_value in hash_tags:
      mapped_hash_tag = MappedHashTag(post_id=post_id, value=hash_tag_value, created_datetime=now)
      session.add(mapped_hash_tag)
    session.commit()

    return post_id
  except sa.exc.IntegrityError:
    session.rollback()
    raise db_util.DbException._chain()


@db_util.use_session
def get_post(session, post_id, now=None):
  now = _utcnow(now)

  try:
    mapped_post = session.query(MappedPost)\
        .filter(MappedPost.id == post_id)\
        .one()
    hash_tags = tuple(row[0] for row in session.query(MappedHashTag.value)\
        .filter(MappedHashTag.post_id == post_id))
    return Post(mapped_post.id,
        mapped_post.creator,
        mapped_post.created_datetime,
        mapped_post.data,
        mapped_post.num_stars,
        hash_tags)
  except sa_orm.exc.NoResultFound:
    return None


@db_util.use_session
def star_post(session, user_id, post_id, now=None):
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


@db_util.use_session
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


@db_util.use_session
def get_all_posts():
  now = _utcnow(now)
  # TODO


@db_util.use_session
def get_posts_for_user(client_id):
  now = _utcnow(now)
  # TODO


@db_util.use_session
def get_post_for_hashtag(hash_tag):
  now = _utcnow(now)
  # TODO

