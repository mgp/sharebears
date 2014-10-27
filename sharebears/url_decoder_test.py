from unittest import TestCase
import urlparse


class UrlDecoderTestCase(TestCase):
  """Base class for testing UrlDecoder instances."""

  def _parse_url(self, url):
    return urlparse.urlparse(url)

  def _is_decodeable_url(self, decoder, url):
    parsed_url = self._parse_url(url)
    return decoder.is_decodeable_url(url, parsed_url)

