import url_decoder
from url_decoder import UrlDecoder, UrlDecoderException


class ImageItem:
  """An image for a RenderableItem."""

  def __init__(self, decoded_url):
    self.url = decoded_url["url"]


class ImageUrlDecoder(UrlDecoder):
  """Embeds an image."""

  @staticmethod
  def name():
    return "image"

  @staticmethod
  def can_decode_url(url, parsed_url):
    parsed_path = parsed_url.path
    return (parsed_path.endswith(".jpeg") or
        parsed_path.endswith(".jpg") or
        parsed_path.endswith(".gif") or
        parsed_path.endswith(".png"))
  
  def decode_url(self, url, parsed_url):
    return { "url": url }

  def item_for_rendering(self, decoded_url):
    return ImageItem(decoded_url)

