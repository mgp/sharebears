import unittest

import db
import db_schema
import db_util


class DbTestCase(unittest.TestCase):
  # Specify an in-memory SQLite database.
  _DATABASE = "sqlite"
  _DATABASE_URI = "sqlite://"
  # Created by setUpClass.
  _engine = None


  @classmethod
  def setUpClass(cls):
    DbTestCase._engine = db_util.init_db(DbTestCase._DATABASE, DbTestCase._DATABASE_URI)

  def setUp(self):
    unittest.TestCase.setUp(self)
    db_schema.create_all_tables(DbTestCase._engine)

  def tearDown(self):
    db_schema.drop_all_tables(DbTestCase._engine)
    unittest.TestCase.tearDown(self)

  # TODO

