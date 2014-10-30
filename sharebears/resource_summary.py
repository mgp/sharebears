import album_item
from url_decoder_image import ImageUrlDecoder
from url_decoder_github import GitHubRepositoryUrlDecoder
from url_decoder_twitter import TwitterTweetUrlDecoder
from url_decoder_youtube import YouTubeUrlDecoder


class ResourceSummary:
  """The resource summary for one or more posts."""

  def __init__(self):
    self.has_images = False
    self.has_tweets = False
    self.youtube_videos = []
    self.has_albums = False
    self.has_github_repos = False

  def __repr__(self):
    return "ResourceSummary(has_images=%s, has_tweets=%s, youtube_videos=%r, has_albums=%s, has_github_repos=%s)" % (
        self.has_images,
        self.has_tweets,
        self.youtube_videos,
        self.has_albums,
        self.has_github_repos)


def _update_summary_for_renderable_item(summary, renderable_item, post_index, item_index):
  renderer_name = renderable_item.get_renderer_name()
  if renderer_name is None:
    return

  if renderer_name == ImageUrlDecoder.name():
    summary.has_images = True
  elif renderer_name == TwitterTweetUrlDecoder.name():
    summary.has_tweets = True
  elif renderer_name == YouTubeUrlDecoder.name():
    summary.youtube_videos.append((renderable_item.item.video_id, post_index, item_index))
  elif renderer_name == album_item._ALBUM_ITEM_TYPE:
    summary.has_albums = True
  elif renderer_name == GitHubRepositoryUrlDecoder.name():
    summary.has_github_repos = True

def _update_summary_for_renderable_post(summary, post, post_index):
  for item_index, renderable_item in enumerate(post.renderable_items):
    _update_summary_for_renderable_item(summary, renderable_item, post_index, item_index)


def summary_for_renderable_post(post):
  """Returns a ResourceSummary for the given RenderablePost instance."""
  summary = ResourceSummary()
  _update_summary_for_renderable_post(summary, post, 0)
  return summary

def summary_for_renderable_post_sequence(post_sequence):
  """Returns a ResourceSummary for the given sequence of RenderablePost instances."""
  summary = ResourceSummary()
  for post_index, post in enumerate(post_sequence):
    _update_summary_for_renderable_post(summary, post, post_index)
  return summary

