import unittest
from datetime import datetime, timedelta

from renderable_item import RenderableItem
import filters


class _FiltersTestDecoder:
  @staticmethod
  def name():
    return "test-decoder"


class FiltersTest(unittest.TestCase):
  def _assert_time_ago_string(self, expected_string, created_datetime, now):
    self.assertEqual(expected_string, filters._get_time_ago_string(created_datetime, now))


  def test_time_ago_string(self):
    now = datetime(2014, 10, 27, 9, 15, 45)

    # In the future.
    created_datetime = now + timedelta(seconds=1)
    self._assert_time_ago_string(filters._JUST_NOW_STRING, created_datetime, now)

    # Preceding year.
    created_datetime = datetime(2013, 1, 1)
    self._assert_time_ago_string("Jan 1, 2013", created_datetime, now)

    # Same year.
    created_datetime = datetime(2014, 1, 1)
    self._assert_time_ago_string("Jan 1", created_datetime, now)

    # Same month.
    created_datetime = datetime(2014, 10, 1)
    self._assert_time_ago_string("Oct 1", created_datetime, now)

    # Preceding day but not within 24 hours.
    created_datetime = datetime(2014, 10, 26)
    self._assert_time_ago_string("Oct 26", created_datetime, now)

    # Preceding day and within 24 hours.
    created_datetime = now - timedelta(hours=23, seconds=1)
    self._assert_time_ago_string("23h ago", created_datetime, now)
    created_datetime = now - timedelta(hours=1, seconds=1)
    self._assert_time_ago_string("1h ago", created_datetime, now)

    # Within 1 hour.
    created_datetime = now - timedelta(minutes=59, seconds=1)
    self._assert_time_ago_string("59m ago", created_datetime, now)
    created_datetime = now - timedelta(minutes=1, seconds=1)
    self._assert_time_ago_string("1m ago", created_datetime, now)

    # Within 1 minute.
    created_datetime = now - timedelta(seconds=59)
    self._assert_time_ago_string("59s ago", created_datetime, now)
    created_datetime = now - timedelta(seconds=1)
    self._assert_time_ago_string("1s ago", created_datetime, now)

    # Same date and time.
    created_datetime = now
    self._assert_time_ago_string(filters._JUST_NOW_STRING, created_datetime, now)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(FiltersTest))
  return suite
 
