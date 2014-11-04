from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from db_schema import Post as MappedPost, Posts, HashTag as MappedHashTag, HashTags, StarredPost as MappedStarredPost, StarredPosts
import db_util
from db_util import DbException


class PaginatedSequence:
  """A sequence of items read from the database.

  This sequence may not represent all items in the sequence.
  Using the pagination values, a client can iterate over all items.
  """

  def __init__(self, items):
    self.items = items

  def __getitem__(self, index):
    return self.items[index]

  def __len__(self):
    return len(self.items)

  def __repr__(self):
    return "PaginatedSequence(items=%r)" % self.items


class Post:
  """A post read from the database."""

  def __init__(self, id, creator, created_datetime, data, is_starred, num_stars, hash_tags):
    self.id = id
    self.creator = creator
    self.created_datetime = created_datetime
    self.data = data
    self.is_starred = is_starred
    self.num_stars = num_stars
    self.hash_tags = hash_tags

  def __repr__(self):
    return "Post(id=%r, creator=%r, created_datetime=%r, data=%r, is_starred=%r, num_stars=%r, hash_tags=%r)" % (
        self.id,
        self.creator,
        self.created_datetime,
        self.data,
        self.is_starred,
        self.num_stars,
        self.hash_tags)


def _utcnow(now):
  """Returns the given time if not None, or datetime.utcnow() otherwise."""
  if now is None:
    return datetime.utcnow()
  return now


@db_util.use_session
def add_post(session, user_id, data, hash_tags, now=None):
  """Creates a new post with the given properties.

  Returns the identifier of the created post.
  """

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


def _make_post(mapped_post, starred_post):
  """Returns a Post constructed from the given MappedPost and hash tags."""
  is_starred = bool(starred_post)
  hash_tags = tuple(mapped_hash_tag.value for mapped_hash_tag in mapped_post.hash_tags)
  return Post(mapped_post.id,
      mapped_post.creator,
      mapped_post.created_datetime,
      mapped_post.data,
      is_starred,
      mapped_post.num_stars,
      hash_tags)


def _get_post_query(session, client_id):
  return session.query(MappedPost, MappedStarredPost)\
      .options(sa_orm.subqueryload(MappedPost.hash_tags))\
      .outerjoin(MappedStarredPost, sa.and_(
        MappedStarredPost.post_id == MappedPost.id,
        MappedStarredPost.user_id == client_id))\


@db_util.use_session
def get_post(session, client_id, post_id, now=None):
  """Returns the post with the given identifier."""

  now = _utcnow(now)

  try:
    result = _get_post_query(session, client_id)\
        .filter(MappedPost.id == post_id)\
        .one()
    return _make_post(*result)
  except sa_orm.exc.NoResultFound:
    return None


@db_util.use_session
def get_posts(session, client_id, now=None):
  """Returns all posts."""

  now = _utcnow(now)

  try:
    results = _get_post_query(session, client_id)\
        .order_by(MappedPost.created_datetime.desc())
    posts = tuple(_make_post(*result) for result in results)
    return PaginatedSequence(posts)
  except sa.exc.IntegrityError:
    session.rollback()
    raise db_util.DbException._chain()


@db_util.use_session
def get_posts_with_hashtag(session, client_id, hash_tag, now=None):
  """Returns all posts with the given hash tag."""

  now = _utcnow(now)

  try:
    results = session.query(MappedHashTag, MappedStarredPost)\
        .options(sa_orm.joinedload(MappedHashTag.post))\
        .outerjoin(MappedStarredPost, sa.and_(
          MappedStarredPost.post_id == MappedHashTag.post_id,
          MappedStarredPost.user_id == client_id))\
        .order_by(MappedHashTag.created_datetime.desc())\
        .filter(MappedHashTag.value == hash_tag)
    posts = tuple(_make_post(mapped_hash_tag.post, mapped_starred_post)
        for mapped_hash_tag, mapped_starred_post in results)
    return PaginatedSequence(posts)
  except sa.exc.IntegrityError:
    session.rollback()
    raise db_util.DbException._chain()


@db_util.use_session
def get_posts_by_user(session, client_id, user_id, now=None):
  """Returns all posts by the given user."""

  now = _utcnow(now)
  try:
    results = _get_post_query(session, client_id)\
        .order_by(MappedPost.created_datetime.desc())\
        .filter(MappedPost.creator == user_id)
    posts = tuple(_make_post(*result) for result in results)
    return PaginatedSequence(posts)
  except sa.exc.IntegrityError:
    session.rollback()
    raise db_util.DbException._chain()


@db_util.use_session
def star_post(session, user_id, post_id, now=None):
  now = _utcnow(now)

  try:
    # Add the user's star for this post.
    starred_post = MappedStarredPost(post_id=post_id,
        user_id=user_id,
        starred_datetime=now)
    session.add(starred_post)
    session.flush()
  except sa.exc.IntegrityError:
    # The user has already starred this post, or this post does not exist.
    session.rollback()
    return None

  # Increment the count of stars for the post.
  session.execute(Posts.update()
      .where(MappedPost.id == post_id)
      .values({MappedPost.num_stars: MappedPost.num_stars + 1}))

  session.commit()


@db_util.use_session
def get_stars(session, post_id, now=None):
  now = _utcnow(now)

  try:
    mapped_starred_posts = session.query(MappedStarredPost.user_id)\
        .order_by(MappedStarredPost.starred_datetime.desc())\
        .filter(MappedStarredPost.post_id == post_id)
    user_ids = tuple(mapped_starred_post.user_id for mapped_starred_post in mapped_starred_posts)
    return PaginatedSequence(user_ids)
  except sa.exc.IntegrityError:
    session.rollback()
    raise db_util.DbException._chain()


@db_util.use_session
def unstar_post(session, user_id, post_id, now=None):
  now = _utcnow(now)

  # Remove the user's star for the post.
  result = session.execute(StarredPosts.delete().where(sa.and_(
      MappedStarredPost.user_id == user_id,
      MappedStarredPost.post_id == post_id)))
  if not result.rowcount:
    # The user has not starred this post.
    session.rollback()
    return

  # Decrement the count of stars for the post.
  session.execute(Posts.update()
      .where(MappedPost.id == post_id)
      .values({MappedPost.num_stars: MappedPost.num_stars - 1}))

  session.commit()

