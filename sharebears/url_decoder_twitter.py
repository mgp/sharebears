import re

from url_decoder import UrlDecoder


class _TwitterUrlDecoder(UrlDecoder):
  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not parsed_url.netloc.startswith("twitter."):
      return False
    return True



class TwitterTimelineItem:
  """A Twitter timeline for a RenderableItem."""

  def __init__(self, decoded_url):
    self.url = decoded_url["url"]


class TwitterTimelineUrlDecoder(_TwitterUrlDecoder):
  """Embeds the timeline of a Twitter user."""

  _PATH_REGEX = re.compile("^/\w+$")

  @staticmethod
  def name():
    return "twitter-timeline"

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not _TwitterUrlDecoder.is_decodeable_url(url, parsed_url):
      return False
    elif not TwitterTimelineUrlDecoder._PATH_REGEX.match(parsed_url.path):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded timeline.
    # See https://dev.twitter.com/web/embedded-timelines
    return { "url": url }

  def item_for_rendering(self, decoded_url):
    return TwitterTimelineItem(decoded_url)



class TwitterTweetItem:
  """A tweet for a RenderableItem."""

  def __init__(self, decoded_url):
    self.url = decoded_url["url"]


class TwitterTweetUrlDecoder(_TwitterUrlDecoder):
  """Embeds a tweet by a Twitter user."""

  _PATH_REGEX = re.compile("^/\w+/status/\w+$")

  @staticmethod
  def name():
    return "twitter-tweet"

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not _TwitterUrlDecoder.is_decodeable_url(url, parsed_url):
      return False
    elif not TwitterTweetUrlDecoder._PATH_REGEX.match(parsed_url.path):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded tweet.
    # See https://dev.twitter.com/web/embedded-tweets
    return { "url": url }

  def item_for_rendering(self, decoded_url):
    return TwitterTweetItem(decoded_url)

