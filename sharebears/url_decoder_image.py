import url_decoder
from url_decoder import UrlDecoder, UrlDecoderException


class ImageUrlDecoder(UrlDecoder):
  """Embeds an image."""

  @staticmethod
  def name():
    return "image"

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    parsed_path = parsed_url.path
    return (parsed_path.endswith(".jpeg") or
        parsed_path.endswith(".jpg") or
        parsed_path.endswith(".gif") or
        parsed_path.endswith(".png"))
  
  def decode_url(self, url, parsed_url):
    return { "url": url }

  def render_decoded_url(self, decoded_url):
    # TODO
    pass

