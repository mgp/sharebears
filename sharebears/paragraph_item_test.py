import itertools
import unittest

import paragraph_item
from renderable_item import RenderableItem


class InsertParagraphsTest(unittest.TestCase):
  def _assert_paragraph(self, renderable_item, expected_child_items):
    self.assertEqual(paragraph_item._PARAGRAPH_ITEM_TYPE, renderable_item.get_renderer_name())

    # Assert that the child items are equal.
    child_items = renderable_item.item.child_items
    self.assertEqual(len(expected_child_items), len(child_items))
    for expected_child_item, child_item in itertools.izip(expected_child_items, child_items):
      self.assertIs(expected_child_item, child_item)

  def _make_other_renderable_item(self):
    return RenderableItem.for_renderer("other-type", None)


  def test_empty_items(self):
    new_items = paragraph_item.insert_paragraphs([])
    self.assertEqual(0, len(new_items))

  def test_only_item_is_text_or_url(self):
    # Assert that a paragraph is created for a single text item.
    items = [RenderableItem.for_text("text")]
    new_items = paragraph_item.insert_paragraphs(items)
    self.assertEqual(1, len(new_items))
    self._assert_paragraph(new_items[0], items)

    # Assert that a paragraph is created for a single word item.
    items = [RenderableItem.for_url("http://url")]
    new_items = paragraph_item.insert_paragraphs(items)
    self.assertEqual(1, len(new_items))
    self._assert_paragraph(new_items[0], items)

  def test_all_items_are_text_or_urls(self):
    # Assert that a paragraph is created for multiple text or URLs.
    text_item0 = RenderableItem.for_text("text0")
    url_item1 = RenderableItem.for_url("http://url1")
    text_item2 = RenderableItem.for_text("text2")

    items = [text_item0, url_item1, text_item2]
    new_items = paragraph_item.insert_paragraphs(items)
    self.assertEqual(1, len(new_items))
    self._assert_paragraph(new_items[0], items)

  def test_split_paragraphs(self):
    text_item0 = RenderableItem.for_text("text0")
    url_item1 = RenderableItem.for_url("http://url1")
    other_item2 = self._make_other_renderable_item()
    text_item3 = RenderableItem.for_text("text3")

    items = [text_item0, url_item1, other_item2, text_item3]
    new_items = paragraph_item.insert_paragraphs(items)
    self.assertEqual(3, len(new_items))
    self._assert_paragraph(new_items[0], [text_item0, url_item1])
    self.assertIs(other_item2, new_items[1])
    self._assert_paragraph(new_items[2], [text_item3])


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(InsertParagraphsTest))
  return suite

