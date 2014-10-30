from renderable_item import RenderableItem
from url_decoder_image import ImageUrlDecoder


_ALBUM_ITEM_TYPE = "album"

def insert_albums(renderable_items):
  """Returns a new list of renderable_items where contiguous ImageItem
  instances are collapsed into an AlbumItem instance.
  """

  if len(renderable_items) < 2:
    # An album contains at least two images.
    return renderable_items

  image_item_type = ImageUrlDecoder.name()

  new_renderable_items = renderable_items[:1]
  for renderable_item in renderable_items[1:]:
    if renderable_item.get_renderer_name() == image_item_type:
      last_renderable_item = new_renderable_items[-1]
      last_renderer_name = last_renderable_item.get_renderer_name()
      if last_renderer_name == _ALBUM_ITEM_TYPE:
        # Append this photo to the ongoing album.
        last_renderable_item.item.image_items.append(renderable_item)
      elif last_renderer_name == image_item_type:
        # Create an album with this image and the preceding image.
        new_renderable_items.pop()
        album = AlbumItem([last_renderable_item, renderable_item])
        album_item = RenderableItem.for_renderer(_ALBUM_ITEM_TYPE, album)
        new_renderable_items.append(album_item)
      else:
        # A following image will create an album.
        new_renderable_items.append(renderable_item)
    else:
      new_renderable_items.append(renderable_item)

  return new_renderable_items



class AlbumItem:
  """An album for a RenderableItem.

  This is composed of multiple ImageItem instances.
  """

  def __init__(self, image_items):
    self.image_items = image_items

