import itertools
import unittest

import album_item
from url_decoder import RenderableItem
from url_decoder_image import ImageItem, ImageUrlDecoder


class InsertAlbumsTest(unittest.TestCase):
  def _make_renderable_image_item(self, url):
    decoded_url = {"url": url }
    image_item = ImageItem(decoded_url)
    return RenderableItem(ImageUrlDecoder.name(), image_item)

  def _make_renderable_item(self):
    return RenderableItem("other-type", None)

  def _assert_album(self, renderable_item, expected_image_items):
    self.assertEqual(renderable_item.type, album_item._ALBUM_ITEM_TYPE)

    # Assert that the image items are equal.
    image_items = renderable_item.item.image_items
    self.assertEqual(len(expected_image_items), len(image_items))
    for expected_image_item, image_item in itertools.izip(expected_image_items, image_items):
      self.assertIs(expected_image_item, image_item)


  def test_empty_items(self):
    new_items = album_item.insert_albums([])
    self.assertEqual(0, len(new_items))

  def test_no_image_items(self):
    items = [self._make_renderable_item() for i in xrange(3)]
    new_items = album_item.insert_albums(items)
    self.assertEqual(len(items), len(new_items))
    for item, new_item in itertools.izip(items, new_items):
      self.assertIs(item, new_item)

  def test_only_item_is_image(self):
    items = [self._make_renderable_image_item("image0")]
    new_items = album_item.insert_albums(items)
    self.assertEqual(1, len(new_items))
    self.assertIs(items[0], new_items[0])

  def test_all_items_are_images(self):
    # Assert that an album is created for only two images.
    image_item0 = self._make_renderable_image_item("image0")
    image_item1 = self._make_renderable_image_item("image1")
    image_items = [image_item0, image_item1]

    new_items = album_item.insert_albums(image_items)
    self.assertEqual(1, len(new_items))
    self._assert_album(new_items[0], image_items)

    # Assert that an album is created for more than two images.
    image_item2 = self._make_renderable_image_item("image2")
    image_items.append(image_item2)
    new_items = album_item.insert_albums(image_items)
    self.assertEqual(1, len(new_items))
    self._assert_album(new_items[0], image_items)

  def test_split_images(self):
    image_item0 = self._make_renderable_image_item("image0")
    image_item1 = self._make_renderable_image_item("image1")
    other_item = self._make_renderable_item()

    items = [image_item0, other_item, image_item1]
    new_items = album_item.insert_albums(items)
    self.assertEqual(len(items), len(new_items))
    for item, new_item in itertools.izip(items, new_items):
      self.assertIs(item, new_item)

  def test_split_albums(self):
    image_item0 = self._make_renderable_image_item("image0")
    image_item1 = self._make_renderable_image_item("image1")
    image_item2 = self._make_renderable_image_item("image2")
    image_item3 = self._make_renderable_image_item("image3")
    other_item = self._make_renderable_item()

    items = [image_item0, image_item1, other_item, image_item2, image_item3]
    new_items = album_item.insert_albums(items)
    self.assertEqual(3, len(new_items))
    self._assert_album(new_items[0], [image_item0, image_item1])
    self.assertIs(other_item, new_items[1])
    self._assert_album(new_items[2], [image_item2, image_item3])


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(InsertAlbumsTest))
  return suite

