from renderable_item import RenderableItem


_PARAGRAPH_ITEM_TYPE = "paragraph"


def insert_paragraphs(renderable_items):
  """Returns a new list of renderable_items where contiguous items of type
  TEXT and URL are collapsed into a ParagraphItem instance.
  """

  new_renderable_items = []
  curr_paragraph = []

  def _end_curr_paragraph():
    if curr_paragraph:
      renderable_item = RenderableItem.for_renderer(_PARAGRAPH_ITEM_TYPE, curr_paragraph.pop())
      new_renderable_items.append(renderable_item)

  for renderable_item in renderable_items:
    item_type = renderable_item.type
    if (item_type == RenderableItem.TEXT_TYPE) or (item_type == RenderableItem.URL_TYPE):
      if not curr_paragraph:
        curr_paragraph.append(ParagraphItem([]))
      curr_paragraph[0].child_items.append(renderable_item)
    else:
      _end_curr_paragraph()
      new_renderable_items.append(renderable_item)
  _end_curr_paragraph()

  return new_renderable_items


class ParagraphItem:
  """A paragraph of text.
  
  This is composed of RenderableItem instances of type TEXT or URL."""

  def __init__(self, child_items):
    self.child_items = child_items

