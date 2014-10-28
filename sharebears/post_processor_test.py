import unittest
import urlparse

from post_processor import PostProcessor
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


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(PostProcessorTest))
  return suite

