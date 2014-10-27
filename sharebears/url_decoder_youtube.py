import re

from url_decoder import UrlDecoder


class YouTubeUrlDecoder(UrlDecoder):
  """Embeds a YouTube video."""

  _QUERY_REGEX = re.compile("^v=\w+$")

  @staticmethod
  def name():
    return "youtube"

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not parsed_url.netloc.startswith("www.youtube."):
      return False
    elif parsed_url.path != "/watch":
      return False
    elif not YouTubeUrlDecoder._QUERY_REGEX.match(parsed_url.query):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded video player.
    # See https://developers.google.com/youtube/player_parameters
    return { "url": url }

  def render_decoded_url(self, decoded_url):
    # TODO
    pass

