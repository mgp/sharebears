from datetime import datetime
import unittest

import db
import db_schema
import db_util


class PostInsertData:
  def __init__(self, user_id, data, hash_tags, now):
    self.user_id = user_id
    self.data = data
    self.hash_tags = hash_tags
    self.now = now

  def __repr__(self):
    return "PostInsertData(user_id=%r, data=%r, hash_tags=%r, now=%r)" % (
        self.user_id,
        self.data,
        self.hash_tags,
        self.now)


class DbTest(unittest.TestCase):
  # Use an in-memory SQLite database.
  _DATABASE = "sqlite"
  _DATABASE_URI = "sqlite://"
  # Created by setUpClass.
  _engine = None


  @classmethod
  def setUpClass(cls):
    DbTest._engine = db_util.init_db(DbTest._DATABASE, DbTest._DATABASE_URI)

  def setUp(self):
    unittest.TestCase.setUp(self)
    db_schema.create_all_tables(DbTest._engine)

  def tearDown(self):
    db_schema.drop_all_tables(DbTest._engine)
    unittest.TestCase.tearDown(self)


  def _add_post(self, insert_data):
    """Inserts the given PostInsertData into the database."""
    self.assertIsNotNone(insert_data)
    post_id = db.add_post(
        insert_data.user_id, insert_data.data, insert_data.hash_tags, now=insert_data.now)
    self.assertIsNotNone(post_id)
    return post_id

  def _assert_post(self, insert_data, actual_post, expected_num_stars=0):
    """Asserts that the given Post contains the given PostInsertData."""

    self.assertIsNotNone(insert_data)
    self.assertIsNotNone(actual_post)

    self.assertIsNotNone(actual_post.id)
    self.assertEqual(insert_data.user_id, actual_post.creator)
    self.assertEqual(insert_data.now, actual_post.created_datetime)
    self.assertEqual(insert_data.data, actual_post.data)
    self.assertSequenceEqual(insert_data.hash_tags, actual_post.hash_tags)
    self.assertEqual(expected_num_stars, actual_post.num_stars)


  def test_get_missing_post(self):
    missing_post_id = "missing_post_id"
    post = db.get_post(missing_post_id)
    self.assertIsNone(post)


  def test_get_post(self):
    # Write the first post by one user.
    hash_tags1 = ["hash_tag1", "hash_tag2"]
    now1 = datetime(2013, 9, 26)
    insert_data1 = PostInsertData("user_id1", "data1", hash_tags1, now1)
    post_id1 = self._add_post(insert_data1)

    # Write the second post by another user.
    hash_tags2 = ["hash_tag3"]
    now2 = datetime(2014, 10, 27)
    insert_data2 = PostInsertData("user_id2", "data2", hash_tags2, now2)
    post_id2 = self._add_post(insert_data2)

    # Assert that the first post is read correctly.
    self._assert_post(insert_data1, db.get_post(post_id1), 0)
    # Assert that the second post is read correctly.
    self._assert_post(insert_data2, db.get_post(post_id2), 0)

    # Get both posts.
    all_posts = db.get_posts()
    self.assertEqual(2, len(all_posts))
    # Assert that the second post is returned first because it is more recent.
    self._assert_post(insert_data2, all_posts[0], 0)
    # Assert that the first post is returned last because it is less recent.
    self._assert_post(insert_data1, all_posts[1], 0)


  def test_get_posts_with_hashtag(self):
    hash_tag1 = "hash_tag1"
    hash_tag2 = "hash_tag2"
    hash_tag3 = "hash_tag3"

    # Write the first post by one user.
    hash_tags1 = [hash_tag1, hash_tag2]
    now1 = datetime(2013, 9, 26)
    insert_data1 = PostInsertData("user_id1", "data1", hash_tags1, now1)
    post_id1 = self._add_post(insert_data1)

    # Write the second post by another user.
    hash_tags2 = [hash_tag2, hash_tag3]
    now2 = datetime(2014, 10, 27)
    insert_data2 = PostInsertData("user_id2", "data2", hash_tags2, now2)
    post_id2 = self._add_post(insert_data2)

    # Only the first post has the first hash tag.
    hash_tag_posts = db.get_posts_with_hashtag(hash_tag1)
    self.assertEqual(1, len(hash_tag_posts))
    self._assert_post(insert_data1, hash_tag_posts[0], 0)
    # Only the second post has the third hash tag.
    hash_tag_posts = db.get_posts_with_hashtag(hash_tag3)
    self.assertEqual(1, len(hash_tag_posts))
    self._assert_post(insert_data2, hash_tag_posts[0], 0)
    # Both posts have the second hash tag. Assert ordering from most recent to least recent.
    hash_tag_posts = db.get_posts_with_hashtag(hash_tag2)
    self.assertEqual(2, len(hash_tag_posts))
    self._assert_post(insert_data2, hash_tag_posts[0], 0)
    self._assert_post(insert_data1, hash_tag_posts[1], 0)


  def test_get_posts_with_missing_hashtag(self):
    now1 = datetime(2013, 9, 26)
    insert_data1 = PostInsertData("user_id1", "data1", ["hash_tag"], now1)
    post_id = self._add_post(insert_data1)
    
    hash_tag_posts = db.get_posts_with_hashtag("missing_hashtag")
    self.assertEqual(0, len(hash_tag_posts))


  def test_get_posts_by_user(self):
    user_id1 = "user_id1"
    user_id2 = "user_id2"

    # Write the first post by the first user.
    now1 = datetime(2012, 8, 25)
    insert_data1 = PostInsertData(user_id1, "data1", ["hash_tag1"], now1)
    post_id1 = self._add_post(insert_data1)

    # Write the second post by the second user.
    now2 = datetime(2013, 9, 26)
    insert_data2 = PostInsertData(user_id2, "data2", ["hash_tag2"], now2)
    post_id2 = self._add_post(insert_data2)

    # Write the third post by the first user.
    now3 = datetime(2014, 10, 27)
    insert_data3 = PostInsertData(user_id1, "data3", [], now3)
    post_id3 = self._add_post(insert_data3)

    # Get both posts for the first user.
    user_posts = db.get_posts_by_user(user_id1)
    self.assertEqual(2, len(user_posts))
    # Assert that the third post is returned first because it is more recent.
    self._assert_post(insert_data3, user_posts[0], 0)
    # Assert that the first post is returned last because it is less recent.
    self._assert_post(insert_data1, user_posts[1], 0)

    # Get the post for the second user.
    user_posts = db.get_posts_by_user(user_id2)
    self.assertEqual(1, len(user_posts))
    self._assert_post(insert_data2, user_posts[0], 0)

  def test_get_posts_by_missing_user(self):
    now1 = datetime(2013, 9, 26)
    insert_data1 = PostInsertData("user_id1", "data1", ["hash_tag"], now1)
    post_id = self._add_post(insert_data1)

    user_posts = db.get_posts_by_user("missing_user_id")
    self.assertEqual(0, len(user_posts))


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(DbTest))
  return suite

