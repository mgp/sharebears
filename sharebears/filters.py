from url_decoder_image import ImageUrlDecoder
from url_decoder_twitter import TwitterTweetUrlDecoder
from url_decoder_youtube import YouTubeUrlDecoder


def _youtube_player_id(video_id):
  return "ytplayer-%s" % video_id

def _is_decoded_type(decoder_type):
  # name must be a static method.
  decoder_name = decoder_type.name()
  return lambda arg: arg.decoder_name == decoder_name


def add_to_environment(environment):
  env_filters = environment.filters

  env_filters["youtubeplayerid"] = _youtube_player_id

  env_filters["isimage"] = _is_decoded_type(ImageUrlDecoder)
  env_filters["istweet"] = _is_decoded_type(TwitterTweetUrlDecoder)
  env_filters["isyoutubevideo"] = _is_decoded_type(YouTubeUrlDecoder)

