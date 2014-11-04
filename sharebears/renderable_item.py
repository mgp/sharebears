class RenderableItem:
  TEXT_TYPE = "text"
  URL_TYPE = "url"
  _RENDERER_TYPE_PREFIX = "renderer-"


  @staticmethod
  def for_text(text):
    """Returns a RenderableItem for text."""
    return RenderableItem(RenderableItem.TEXT_TYPE, text)

  @staticmethod
  def for_url(url):
    """Returns a RenderableItem for an unrecognized URL."""
    return RenderableItem(RenderableItem.URL_TYPE, url)

  @staticmethod
  def for_renderer(renderer_name, item):
    """Returns a RenderableItem for a renderer with the given name."""
    renderer_type = "%s%s" % (
        RenderableItem._RENDERER_TYPE_PREFIX, renderer_name)
    return RenderableItem(renderer_type, item)


  def __init__(self, type, item):
    self.type = type
    self.item = item

  def __repr__(self):
    return "RenderableItem(type=%r, item=%r)" % (self.type, self.item)

  def get_renderer_name(self):
    if self.type.startswith(RenderableItem._RENDERER_TYPE_PREFIX):
      return self.type[len(RenderableItem._RENDERER_TYPE_PREFIX):]
    return None



class RenderablePost:
  """A post that is ready for rendering."""

  def __init__(self, id, creator, created_datetime, renderable_items, is_starred, num_stars, hash_tags):
    self.id = id
    self.creator = creator
    self.created_datetime = created_datetime
    self.renderable_items = renderable_items
    self.is_starred = is_starred
    self.num_stars = num_stars
    self.hash_tags = hash_tags

  def __repr__(self):
    return "RenderablePost(id=%r, creator=%r, created=%r, items=%r, is_starred=%r, num_stars=%r, hash_tags=%r)" % (
        self.id,
        self.creator,
        self.created_datetime,
        self.renderable_items,
        self.is_starred,
        self.num_stars,
        self.hash_tags)

