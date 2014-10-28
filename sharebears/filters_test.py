import unittest

from url_decoder import RenderableItem
import filters


class _FiltersTestDecoder:
  @staticmethod
  def name():
    return "test-decoder"


class FiltersTest(unittest.TestCase):
  def test_is_decoded_type(self):
    type_filter = filters._is_decoded_type(_FiltersTestDecoder)
    filter_name = _FiltersTestDecoder.name()

    # Pass an URL with a different filter name.
    renderable_url = RenderableItem("different-decoder-name", None)
    self.assertFalse(type_filter(renderable_url))
    # Pass an URL with the same filter name.
    renderable_url = RenderableItem(filter_name, None)
    self.assertTrue(type_filter(renderable_url))


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(FiltersTest))
  return suite
 
