import paragraph_item
from renderable_item import RenderableItem
from url_decoder_image import ImageUrlDecoder
from url_decoder_twitter import TwitterTweetUrlDecoder
from url_decoder_youtube import YouTubeUrlDecoder


def _youtube_player_id(video_id):
  return "ytplayer-%s" % video_id

def _has_renderer(renderer_name):
  """Returns a function that returns whether a RendererItem has the given renderer name."""
  return lambda item: item.get_renderer_name() == renderer_name

def _is_decoded_type(decoder_type):
  # name must be a static method.
  decoder_name = decoder_type.name()
  return lambda arg: arg.type == decoder_name


def add_to_environment(environment):
  env_filters = environment.filters

  env_filters["youtubeplayerid"] = _youtube_player_id

  env_filters["isparagraph"] = _has_renderer(paragraph_item._PARAGRAPH_ITEM_TYPE)
  env_filters["istext"] = lambda item: item.type == RenderableItem.TEXT_TYPE
  env_filters["isurl"] = lambda item: item.type == RenderableItem.URL_TYPE

  env_filters["isimage"] = _has_renderer(ImageUrlDecoder.name())
  env_filters["istweet"] = _has_renderer(TwitterTweetUrlDecoder.name())
  env_filters["isyoutubevideo"] = _has_renderer(YouTubeUrlDecoder.name())

  # TODO(mgp)
  # env_filters["isalbum"] = None

