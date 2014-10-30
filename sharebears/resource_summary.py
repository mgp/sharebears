import album_item
from url_decoder_twitter import TwitterTweetUrlDecoder
from url_decoder_youtube import YouTubeUrlDecoder


class ResourceSummary:
  """The resource summary for one or more posts."""

  def __init__(self):
    self.has_tweets = False
    self.youtube_video_ids = []
    self.has_albums = False

  def __repr__(self):
    return "ResourceSummary(has_tweets=%s, youtube_video_ids=%r, has_albums=%s)" % (
        self.has_tweets,
        self.youtube_ids,
        self.has_albums)


def _update_summary_for_renderable_item(summary, renderable_item):
  renderer_name = renderable_item.get_renderer_name()
  if renderer_name is None:
    return

  if renderer_name == TwitterTweetUrlDecoder.name():
    summary.has_tweets = True
  elif renderer_name == YouTubeUrlDecoder.name():
    summary.youtube_video_ids.append(renderable_item.item.video_id)
  elif renderer_name == album_item._ALBUM_ITEM_TYPE:
    summary.has_albums = True

def _update_summary_for_renderable_post(summary, post):
  for renderable_item in post.renderable_items:
    _update_summary_for_renderable_item(summary, renderable_item)


def summary_for_renderable_post(post):
  """Returns a ResourceSummary for the given RenderablePost instance."""
  summary = ResourceSummary()
  _update_summary_for_renderable_post(summary, post)
  return summary

def summary_for_renderable_post_sequence(post_sequence):
  """Returns a ResourceSummary for the given sequence of RenderablePost instances."""
  summary = ResourceSummary()
  for post in post_sequence:
    _update_summary_for_renderable_post(summary, post)
  return summary

