import unittest

from url_decoder_test import UrlDecoderTestCase
from url_decoder_twitter import TwitterTimelineUrlDecoder, TwitterTweetUrlDecoder


class TwitterTimelineUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.url_decoder = TwitterTimelineUrlDecoder()

  def test_can_decode_url(self):
    # Invalid netloc.
    self.assertFalse(self._can_decode_url(
        self.url_decoder, "https://invalid.twitter.com/omgitsmgp"))
    # Invalid path.
    self.assertFalse(self._can_decode_url(
        self.url_decoder, "https://twitter.com/"))
    self.assertFalse(self._can_decode_url(
        self.url_decoder, "https://twitter.com/omgitsmgp/status/524646360750891008"))

    # Valid URL.
    self.assertTrue(self._can_decode_url(
        self.url_decoder, "https://twitter.com/omgitsmgp"))

  def test_decode_url(self):
    url = "https://twitter.com/omgitsmgp"
    parsed_url = self._parse_url(url)
    expected_dict = { "url": url }
    self.assertDictEqual(expected_dict, self.url_decoder.decode_url(url, parsed_url))

  def test_item_for_rendering(self):
    url = "https://twitter.com/omgitsmgp"
    decoded_url = { "url": url }
    item = self.url_decoder.item_for_rendering(decoded_url)
    self.assertEqual(url, item.url)


class TwitterTweetUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.url_decoder = TwitterTweetUrlDecoder()

  def test_can_decode_url(self):
    # Invalid netloc.
    self.assertFalse(self._can_decode_url(
        self.url_decoder, "https://invalid.twitter.com/omgitsmgp/status/524646360750891008"))
    # Invalid path.
    self.assertFalse(self._can_decode_url(
        self.url_decoder, "https://twitter.com/"))
    self.assertFalse(self._can_decode_url(
        self.url_decoder, "https://twitter.com/omgitsmgp"))

    # Valid URL.
    self.assertTrue(self._can_decode_url(
        self.url_decoder, "https://twitter.com/omgitsmgp/status/524646360750891008"))

  def test_decode_url(self):
    url = "https://twitter.com/omgitsmgp/status/524646360750891008"
    parsed_url = self._parse_url(url)
    expected_dict = { "url": url }
    self.assertDictEqual(expected_dict, self.url_decoder.decode_url(url, parsed_url))

  def test_item_for_rendering(self):
    url = "https://twitter.com/omgitsmgp/status/524646360750891008"
    decoded_url = { "url": url }
    item = self.url_decoder.item_for_rendering(decoded_url)
    self.assertEqual(url, item.url)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TwitterTimelineUrlDecoderTest))
  suite.addTest(unittest.makeSuite(TwitterTweetUrlDecoderTest))
  return suite

