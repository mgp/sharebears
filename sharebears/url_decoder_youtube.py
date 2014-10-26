from url_decoder import UrlDecoder


class YouTubeUrlDecoder(UrlDecoder):
  def name(self):
    return "youtube"

  def is_decodeable_url(self, url, parsed_url):
    return parsed_url.netloc.startswith("www.youtube.")

  def decode_url(self, url, parsed_url):
    # Use an embedded video player.
    # See https://developers.google.com/youtube/player_parameters
    return { "url": url }

  def render_decoded_url(self, decoded_url):
    # TODO
    pass

