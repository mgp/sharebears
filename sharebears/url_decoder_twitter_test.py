from url_decoder_test import UrlDecoderTestCase
from url_decoder_twitter import TwitterTimelineUrlDecoder, TwitterTweetUrlDecoder


class TwitterTimelineUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.url_decoder = TwitterTimelineUrlDecoder()

  def test_is_decodeable_url(self):
    # Invalid netloc.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://invalid.twitter.com/omgitsmgp"))
    # Invalid path.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://twitter.com/"))
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://twitter.com/omgitsmgp/status/524646360750891008"))

    # Valid URL.
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://twitter.com/omgitsmgp"))

  def test_decode_url(self):
    url = "https://twitter.com/omgitsmgp"
    parsed_url = self._parse_url(url)
    expected_dict = { "url": url }
    self.assertDictEqual(expected_dict, self.url_decoder.decode_url(url, parsed_url))


# TODO: Test TwitterTweetUrlDecoder

