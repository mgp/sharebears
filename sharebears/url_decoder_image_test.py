from url_decoder_test import UrlDecoderTestCase
from url_decoder_image import ImageUrlDecoder


class ImageUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.url_decoder = ImageUrlDecoder()

  def test_is_decodeable_url(self):
    # Missing extension.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://www.khanacademy.org/images/image"))
    # Unknown extension.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://www.khanacademy.org/images/image.abc"))

    # Valid extensions.
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://www.khanacademy.org/images/image.jpeg"))
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://www.khanacademy.org/images/image.jpg"))
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://www.khanacademy.org/images/image.gif"))
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://www.khanacademy.org/images/image.png"))

  def test_decode_url(self):
    url = "https://www.khanacademy.org/images/image.png"
    parsed_url = self._parse_url(url)
    expected_dict = { "url": url }
    self.assertDictEqual(expected_dict, self.url_decoder.decode_url(url, parsed_url))

