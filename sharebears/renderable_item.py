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
    """Returns a RenderableItem for a bare URL."""
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

  def get_renderer_name(self):
    if self.type.startswith(RenderableItem._RENDERER_TYPE_PREFIX):
      return self.type[len(RenderableItem._RENDERER_TYPE_PREFIX):]
    return None

