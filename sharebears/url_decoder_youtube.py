import re
import urlparse

from url_decoder import UrlDecoder


_QUERY_REGEX = re.compile("^v=(?P<videoId>\w+)$")


class YouTubeItem:
  """A YouTube video for a RenderableItem."""

  def __init__(self, decoded_url):
    self.url = decoded_url["url"]

    # Extract the video identifier from the URL.
    parsed_url = urlparse.urlparse(self.url)
    match = _QUERY_REGEX.match(parsed_url.query)
    self.video_id = match.group("videoId")


class YouTubeUrlDecoder(UrlDecoder):
  """Embeds a YouTube video."""

  @staticmethod
  def name():
    return "youtube"

  @staticmethod
  def can_decode_url(url, parsed_url):
    if not parsed_url.netloc.startswith("www.youtube."):
      return False
    elif parsed_url.path != "/watch":
      return False
    elif not _QUERY_REGEX.match(parsed_url.query):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded video player.
    # See https://developers.google.com/youtube/player_parameters
    return { "url": url }

  def item_for_rendering(self, decoded_url):
    return YouTubeItem(decoded_url)

