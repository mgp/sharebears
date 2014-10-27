from unittest import TestCase

import parser


class _ParserTestDecoder:
  def __init__(self, matched_url_prefix):
    self.matched_url_prefix = matched_url_prefix

  def matches_url(self, url):
    return url.startswith(self.matched_url_prefix)


class ParserTest(TestCase):
  def setUp(self):
    TestCase.setUp(self)

    self.decoder0 = _ParserTestDecoder("http://decoder0")
    self.decoder1 = _ParserTestDecoder("http://decoder1")
    self.parser = parser.Parser([self.decoder0, self.decoder1])


  def _assert_text_token(self, token, expected_text):
    self.assertEqual(parser.Token.TEXT, token.type)
    self.assertEqual(expected_text, token.value)

  def _assert_url_token(self, token, expected_url, expected_decoder=None):
    self.assertEqual(parser.Token.URL, token.type)
    self.assertEqual(expected_url, token.value)
    self.assertIs(expected_decoder, token.decoder)

  def _assert_hash_tag_token(self, token, expected_hash_tag):
    self.assertEqual(parser.Token.HASH_TAG, token.type)
    self.assertEqual(expected_hash_tag, token.value)


  def _join(self, *values):
    return " ".join(values)

  def test_parse_empty(self):
    tokens = self.parser.parse("")
    self.assertEqual(0, len(tokens))

    tokens = self.parser.parse("   ")
    self.assertEqual(0, len(tokens))

  def test_parse_only_hash_tags(self):
    tokens = self.parser.parse("#ht0")
    self.assertEqual(1, len(tokens))
    self._assert_hash_tag_token(tokens[0], "ht0")

    tokens = self.parser.parse("#ht0 #ht1 #ht2")
    self.assertEqual(3, len(tokens))
    self._assert_hash_tag_token(tokens[0], "ht0")
    self._assert_hash_tag_token(tokens[1], "ht1")
    self._assert_hash_tag_token(tokens[2], "ht2")

  def test_parse_only_text(self):
    tokens = self.parser.parse("text0")
    self.assertEqual(1, len(tokens))
    self._assert_text_token(tokens[0], "text0")

    tokens = self.parser.parse("text0 text1 text2")
    self.assertEqual(3, len(tokens))
    self._assert_text_token(tokens[0], "text0")
    self._assert_text_token(tokens[1], "text1")
    self._assert_text_token(tokens[2], "text2")

  def test_parse_only_unrecognized_urls(self):
    url0 = "http://url0"
    tokens = self.parser.parse(url0)
    self.assertEqual(1, len(tokens))
    self._assert_url_token(tokens[0], url0)

    url1 = "http://url1"
    url2 = "http://url2"
    tokens = self.parser.parse(self._join(url0, url1, url2))
    self.assertEqual(3, len(tokens))
    self._assert_url_token(tokens[0], url0)
    self._assert_url_token(tokens[1], url1)
    self._assert_url_token(tokens[2], url2)

  def test_parse_only_recognized_urls(self):
    url0 = "http://decoder0/path0"
    url1 = "http://decoder1/path1"
    tokens = self.parser.parse(self._join(url0, url1))
    self.assertEqual(2, len(tokens))
    self._assert_url_token(tokens[0], url0, self.decoder0)
    self._assert_url_token(tokens[1], url1, self.decoder1)

  def test_separate_hash_tags(self):
    # Precede the hash tags with text.
    tokens = self.parser.parse("text0 #ht1 #ht2")
    self.assertEqual(3, len(tokens))
    self._assert_text_token(tokens[0], "text0")
    self._assert_hash_tag_token(tokens[1], "ht1")
    self._assert_hash_tag_token(tokens[2], "ht2")

    # Precede the hash tags with a URL.
    url0 = "http://url0"
    tokens = self.parser.parse("%s #ht1 #ht2" % url0)
    self.assertEqual(3, len(tokens))
    self._assert_url_token(tokens[0], url0)
    self._assert_hash_tag_token(tokens[1], "ht1")
    self._assert_hash_tag_token(tokens[2], "ht2")

  def test_alternate_text_and_urls(self):
    # An URL between two text tokens.
    tokens = self.parser.parse("text0 http://url1 text2")
    self.assertEqual(3, len(tokens))
    self._assert_text_token(tokens[0], "text0")
    self._assert_url_token(tokens[1], "http://url1")
    self._assert_text_token(tokens[2], "text2")

    # Text between two URL tokens.
    tokens = self.parser.parse("http://url0 text1 http://url2")
    self.assertEqual(3, len(tokens))
    self._assert_url_token(tokens[0], "http://url0")
    self._assert_text_token(tokens[1], "text1")
    self._assert_url_token(tokens[2], "http://url2")

