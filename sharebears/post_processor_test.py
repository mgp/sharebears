import unittest
import urlparse

import paragraph_item
from post_processor import PostProcessor
from renderable_item import RenderableItem
from test_util import TestDecoder

class PostProcessorTest(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    self.decoder0 = TestDecoder("decoder0", "http://decoder0")
    self.decoder1 = TestDecoder("decoder1", "http://decoder1")
    self.processor = PostProcessor([self.decoder0, self.decoder1])


  def _assert_element(self, element, expected_type, expected_value):
    self.assertEqual(expected_type, element["type"])
    self.assertEqual(expected_value, element["value"])

  def _assert_text_element(self, element, expected_text):
    self._assert_element(element, PostProcessor._TEXT_TYPE, expected_text)

  def _assert_unrecognized_url_element(self, element, expected_url):
    self._assert_element(element, PostProcessor._URL_TYPE, expected_url)

  def _assert_recognized_url_element(self, element, expected_url, expected_url_decoder):
    self.assertIn(expected_url_decoder.name(), element["type"])
    parsed_url = urlparse.urlparse(expected_url)
    expected_decoded_url = expected_url_decoder.decode_url(expected_url, parsed_url)
    self.assertEqual(expected_decoded_url, element["value"])


  def test_process_empty(self):
    processed_post = self.processor.process("")
    self.assertEqual(0, len(processed_post.data))
    self.assertEqual(0, len(processed_post.hash_tags))

    processed_post = self.processor.process("   ")
    self.assertEqual(0, len(processed_post.data))
    self.assertEqual(0, len(processed_post.hash_tags))

  def test_process_only_text(self):
    string = "text0 text1"
    processed_post = self.processor.process(string)
    self.assertEqual(2, len(processed_post.data))
    self._assert_text_element(processed_post.data[0], "text0")
    self._assert_text_element(processed_post.data[1], "text1")
    self.assertEqual(0, len(processed_post.hash_tags))

  def test_process_only_hash_tags(self):
    string = "#ht0 #ht1"
    processed_post = self.processor.process(string)
    self.assertSequenceEqual(["ht0", "ht1"], processed_post.hash_tags)
    self.assertEqual(0, len(processed_post.data))

  def test_process_only_unrecognized_urls(self):
    string = "http://url0 http://url1"
    processed_post = self.processor.process(string)
    self.assertEqual(2, len(processed_post.data))
    self._assert_unrecognized_url_element(processed_post.data[0], "http://url0")
    self._assert_unrecognized_url_element(processed_post.data[1], "http://url1")
    self.assertEqual(0, len(processed_post.hash_tags))

  def test_process_only_recognized_urls(self):
    url0 = "http://decoder0/path0"
    url1 = "http://decoder1/path1"
    string = "%s %s" % (url0, url1)
    processed_post = self.processor.process(string)
    self.assertEqual(2, len(processed_post.data))
    self._assert_recognized_url_element(processed_post.data[0], url0, self.decoder0)
    self._assert_recognized_url_element(processed_post.data[1], url1, self.decoder1)
    self.assertEqual(0, len(processed_post.hash_tags))


  def _assert_text_item(self, renderable_item, expected_text):
    self.assertEqual(RenderableItem.TEXT_TYPE, renderable_item.type)
    self.assertEqual(expected_text, renderable_item.item)

  def _assert_url_item(self, renderable_item, expected_url):
    self.assertEqual(RenderableItem.URL_TYPE, renderable_item.type)
    self.assertEqual(expected_url, renderable_item.item)

  def _assert_decoded_url_item(self, renderable_item, decoded_url, expected_decoder):
    expected_item = expected_decoder.item_for_rendering(decoded_url)
    self.assertEqual(expected_decoder.name(), renderable_item.get_renderer_name())
    self.assertEqual(expected_item, renderable_item.item)


  def test_render_empty(self):
    renderable_items = self.processor.renderable_items([])
    self.assertEqual(0, len(renderable_items))

  def test_render_only_text(self):
    data = [
        PostProcessor._make_data_element(PostProcessor._TEXT_TYPE, "text0"),
        PostProcessor._make_data_element(PostProcessor._TEXT_TYPE, "text1")
    ]
    renderable_items = self.processor.renderable_items(data)
    # One paragraph should be returned.
    self.assertEqual(1, len(renderable_items))
    renderable_item = renderable_items[0]
    self.assertEqual(paragraph_item._PARAGRAPH_ITEM_TYPE, renderable_item.get_renderer_name())

    # The unrecognized URLs should be its children.
    paragraph_child_items = renderable_item.item.child_items
    self.assertEqual(2, len(paragraph_child_items))
    self._assert_text_item(paragraph_child_items[0], "text0")
    self._assert_text_item(paragraph_child_items[1], "text1")

  def test_render_only_unrecognized_urls(self):
    data = [
        PostProcessor._make_data_element(PostProcessor._URL_TYPE, "http://url0"),
        PostProcessor._make_data_element(PostProcessor._URL_TYPE, "http://url1")
    ]
    renderable_items = self.processor.renderable_items(data)

    # One paragraph should be returned.
    self.assertEqual(1, len(renderable_items))
    renderable_item = renderable_items[0]
    self.assertEqual(paragraph_item._PARAGRAPH_ITEM_TYPE, renderable_item.get_renderer_name())

    # The unrecognized URLs should be its children.
    paragraph_child_items = renderable_item.item.child_items
    self.assertEqual(2, len(paragraph_child_items))
    self._assert_url_item(paragraph_child_items[0], "http://url0")
    self._assert_url_item(paragraph_child_items[1], "http://url1")

  def test_render_only_recognized_url(self):
    url0 = "http://decoder0/path0"
    url1 = "http://decoder1/path1"
    decoder0_type = PostProcessor._type_for_decoder(self.decoder0)
    decoder1_type = PostProcessor._type_for_decoder(self.decoder1)
    data = [
        PostProcessor._make_data_element(decoder0_type, url0),
        PostProcessor._make_data_element(decoder1_type, url1)
    ]
    renderable_items = self.processor.renderable_items(data)
    self.assertEqual(2, len(renderable_items))
    self._assert_decoded_url_item(renderable_items[0], url0, self.decoder0)
    self._assert_decoded_url_item(renderable_items[1], url1, self.decoder1)



def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(PostProcessorTest))
  return suite

