import unittest
import urlparse

import url_decoder


class UrlDecoderTestCase(unittest.TestCase):
  """Base class for testing UrlDecoder instances."""

  def _parse_url(self, url):
    return urlparse.urlparse(url)

  def _is_decodeable_url(self, decoder, url):
    parsed_url = self._parse_url(url)
    return decoder.is_decodeable_url(url, parsed_url)


class FilterJsonTestCase(unittest.TestCase):
  def test_filter_json(self):
    json = { "cat": "meow", "dog": "woof", "cow": "moo" }
    filtered_json = url_decoder.filter_json(json, "cat", "dog", "flamingo")
    expected_json = { "cat": "meow", "dog": "woof" }
    self.assertDictEqual(expected_json, filtered_json)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(FilterJsonTestCase))
  return suite

