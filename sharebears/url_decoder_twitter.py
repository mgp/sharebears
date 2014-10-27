import re

from url_decoder import UrlDecoder


class _TwitterUrlDecoder(UrlDecoder):
  def is_decodeable_url(self, url, parsed_url):
    if not parsed_url.netloc.startswith("twitter."):
      return False
    return True


class TwitterTimelineUrlDecoder(_TwitterUrlDecoder):
  """Embeds the timeline of a Twitter user."""

  _PATH_REGEX = re.compile("^/\w+$")

  def name(self):
    return "twitter-timeline"

  def is_decodeable_url(self, url, parsed_url):
    if not _TwitterUrlDecoder.is_decodeable_url(self, url, parsed_url):
      return False
    elif not TwitterTimelineUrlDecoder._PATH_REGEX.match(parsed_url.path):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded timeline.
    # See https://dev.twitter.com/web/embedded-timelines
    return { "url": url }

  def render_decoded_url(self, decoded_url):
    # TODO
    pass


class TwitterTweetUrlDecoder(_TwitterUrlDecoder):
  """Embeds a tweet by a Twitter user."""

  _PATH_REGEX = re.compile("^/\w+/status/\w+$")

  def name(self):
    return "twitter-tweet"

  def is_decodeable_url(self, url, parsed_url):
    if not _TwitterUrlDecoder.is_decodeable_url(self, url, parsed_url):
      return False
    elif not TwitterTweetUrlDecoder._PATH_REGEX.match(parsed_url.path):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded tweet.
    # See https://dev.twitter.com/web/embedded-tweets
    return { "url": url }

  def render_decoded_url(self, decoded_url):
    # TODO
    pass

