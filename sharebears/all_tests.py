import unittest

import parser_test
import url_decoder_github_test
import url_decoder_image_test
import url_decoder_test
import url_decoder_twitter_test
import url_decoder_youtube_test


def suite():
  suite = unittest.TestSuite()
  suite.addTest(parser_test.suite())
  suite.addTest(url_decoder_github_test.suite())
  suite.addTest(url_decoder_image_test.suite())
  suite.addTest(url_decoder_test.suite())
  suite.addTest(url_decoder_twitter_test.suite())
  suite.addTest(url_decoder_youtube_test.suite())
  return suite

def _main():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == "__main__":
  _main()

