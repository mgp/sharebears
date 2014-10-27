import unittest

from url_decoder_test import UrlDecoderTestCase
from url_decoder_youtube import YouTubeUrlDecoder


class YouTubeUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.url_decoder = YouTubeUrlDecoder()

  def test_is_decodeable_url(self):
    # Invalid netloc.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://invalid.youtube.com/watch?v=JC82Il2cjqA"))
    # Invalid path.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://www.youtube.com"))
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://youtube.com/invalid?v=JC82Il2cjqA"))
    # Invalid query string.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://youtube.com/watch?invalid=JC82Il2cjqA"))

    # Valid URL.
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://www.youtube.com/watch?v=JC82Il2cjqA"))

  def test_decode_url(self):
    url = "https://www.youtube.com/watch?v=JC82Il2cjqA"
    parsed_url = self._parse_url(url)
    expected_dict = { "url": url }
    self.assertDictEqual(expected_dict, self.url_decoder.decode_url(url, parsed_url))


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(YouTubeUrlDecoderTest))
  return suite

