import unittest

from renderable_item import RenderableItem


class RenderableItemTest(unittest.TestCase):
  def test_text_type(self):
    text = "text"
    item = RenderableItem.for_text(text)
    self.assertEqual(RenderableItem.TEXT_TYPE, item.type)
    self.assertEqual(text, item.item)
    self.assertIsNone(item.get_renderer_name())

  def test_url_type(self):
    url = "https://www.khanacademy.org/"
    item = RenderableItem.for_url(url)
    self.assertEqual(RenderableItem.URL_TYPE, item.type)
    self.assertEqual(url, item.item)
    self.assertIsNone(item.get_renderer_name())

  def test_custom_type(self):
    renderer_name = "renderer-name-value"
    item_value = "item-value"
    item = RenderableItem.for_renderer(renderer_name, item_value)
    self.assertEqual(renderer_name, item.get_renderer_name())


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(RenderableItemTest))
  return suite

