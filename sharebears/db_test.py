from datetime import datetime
import unittest

import db
import db_schema
import db_util


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


  def _assert_post(self, post, creator, created_datetime, data, num_stars, hash_tags):
    self.assertIsNotNone(post)
    self.assertEqual(creator, post.creator)
    self.assertEqual(created_datetime, post.created_datetime)
    self.assertEqual(data, post.data)
    self.assertEqual(num_stars, post.num_stars)
    self.assertSequenceEqual(hash_tags, post.hash_tags)


  def test_get_missing_post(self):
    missing_post_id = "missing_post_id"
    post = db.get_post(missing_post_id)
    self.assertIsNone(post)


  def test_get_post(self):
    hash_tag1 = "hash_tag1"
    hash_tag2 = "hash_tag2"
    hash_tag3 = "hash_tag3"

    # Write the first post by one user.
    user_id1 = "user_id1"
    data1 = "data1"
    hash_tags1 = [hash_tag1, hash_tag2]
    now1 = datetime(2013, 9, 26)
    post_id1 = db.add_post(user_id1, data1, hash_tags1, now=now1)
    self.assertIsNotNone(post_id1)

    # Write the second post by another user.
    user_id2 = "user_id2"
    data2 = "data2"
    hash_tags2 = [hash_tag2, hash_tag3]
    now2 = datetime(2014, 10, 27)
    post_id2 = db.add_post(user_id2, data2, hash_tags2, now=now2)
    self.assertIsNotNone(post_id2)

    # Assert that the first post is read correctly.
    post1 = db.get_post(post_id1)
    self._assert_post(post1, user_id1, now1, data1, 0, hash_tags1)
    # Assert that the second post is read correctly.
    post2 = db.get_post(post_id2)
    self._assert_post(post2, user_id2, now2, data2, 0, hash_tags2)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(DbTest))
  return suite

