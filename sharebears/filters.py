import album_item
import paragraph_item
from renderable_item import RenderableItem
from url_decoder_github import GitHubRepositoryUrlDecoder
from url_decoder_image import ImageUrlDecoder
from url_decoder_twitter import TwitterTweetUrlDecoder
from url_decoder_youtube import YouTubeUrlDecoder


def _youtube_player_id(video_id, post_id=0, item_id=0):
  return "ytplayer-%s-%s-%s" % (video_id, post_id, item_id)

def _has_renderer(renderer_name):
  """Returns a function that returns whether a RendererItem has the given renderer name."""
  return lambda item: item.get_renderer_name() == renderer_name


_SECONDS_PER_HOUR = 60 * 60
_SECONDS_PER_MINUTE = 60

def _get_day_components(created_timedelta):
  seconds = created_timedelta.seconds
  # Get the number of hours.
  hours = seconds / _SECONDS_PER_HOUR
  seconds %= _SECONDS_PER_HOUR

  # Get the number of minutes.
  minutes = seconds / _SECONDS_PER_MINUTE
  seconds %= _SECONDS_PER_MINUTE

  return (hours, minutes, seconds)


_JUST_NOW_STRING = "just now"

def _get_time_ago_string(created_datetime, now):
  if created_datetime > now:
    return _JUST_NOW_STRING

  created_timedelta = now - created_datetime
  if created_timedelta.days > 0:
    # Avoid using strftime with %d because it returns a leading zero.
    month_name = created_datetime.strftime("%b")
    if created_datetime.year == now.year:
      return "%s %s" % (month_name, created_datetime.day)
    else:
      return "%s %s, %s" % (month_name, created_datetime.day, created_datetime.year)

  hours, minutes, seconds = _get_day_components(created_timedelta)
  if hours > 0:
    return "%sh ago" % hours
  elif minutes > 0:
    return "%sm ago" % minutes
  elif seconds > 0:
    return "%ss ago" % seconds
  else:
    return _JUST_NOW_STRING


def add_to_environment(environment):
  env_filters = environment.filters

  env_filters["timeagostring"] = _get_time_ago_string

  env_filters["youtubeplayerid"] = _youtube_player_id

  env_filters["isparagraph"] = _has_renderer(paragraph_item._PARAGRAPH_ITEM_TYPE)
  env_filters["istext"] = lambda item: item.type == RenderableItem.TEXT_TYPE
  env_filters["isurl"] = lambda item: item.type == RenderableItem.URL_TYPE

  env_filters["isimage"] = _has_renderer(ImageUrlDecoder.name())
  env_filters["istweet"] = _has_renderer(TwitterTweetUrlDecoder.name())
  env_filters["isyoutubevideo"] = _has_renderer(YouTubeUrlDecoder.name())
  env_filters["isalbum"] = _has_renderer(album_item._ALBUM_ITEM_TYPE)
  env_filters["isgithubrepo"] = _has_renderer(GitHubRepositoryUrlDecoder.name())

