from url_decoder_test import UrlDecoderTestCase
from url_decoder_github import GitHubRepositoryUrlDecoder, GitHubCommitUrlDecoder, GitHubGistUrlDecoder


class _GitHubTestClient:
  def __init__(self):
    self.get_repository_args = []
    self.get_commit_args = []

  def get_repository(self, *pargs):
    self.get_repository_args.append(pargs)

    owner_json = { "login": "mgp" }
    return { "owner": owner_json, "name": "repo-name" }

  def get_commit(self, *pargs):
    self.get_commit_args.append(pargs)

    return { "sha": "a8b7818", "message": "Initial commit" }


class GitHubRepositoryUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    test_client = _GitHubTestClient()
    self.url_decoder = GitHubRepositoryUrlDecoder(test_client)

  def test_is_decodeable_url(self):
    # Invalid netloc.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://invalid.github.com/mgp/sharebears"))
    # Invalid path.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://github.com/"))
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://github.com/mgp"))
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://github.com/mgp/sharebears/wiki"))

    # Valid URL.
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://github.com/mgp/sharebears"))

  def test_decode_url(self):
    # TODO
    pass


class GitHubCommitUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    test_client = _GitHubTestClient()
    self.url_decoder = GitHubCommitUrlDecoder(test_client)

  def test_is_decodeable_url(self):
    # Invalid netloc.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://invalid.github.com/mgp/sharebears/commit/a8b7818"))
    # Invalid path.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://github.com/"))
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://github.com/mgp/sharebears/commit"))

    # Valid URL.
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://github.com/mgp/sharebears/commit/a8b7818"))

  def test_decode_url(self):
    # TODO
    pass


class GitHubGistUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.url_decoder = GitHubGistUrlDecoder()

  def test_is_decodeable_url(self):
    # Invalid netloc.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://invalid.gist.github.com/mgp/92b50ae3e1b1b46eadab"))
    # Invalid path.
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://gist.github.com/"))
    self.assertFalse(self._is_decodeable_url(
        self.url_decoder, "https://gist.github.com/mgp"))

    # Valid URL.
    self.assertTrue(self._is_decodeable_url(
        self.url_decoder, "https://gist.github.com/mgp/92b50ae3e1b1b46eadab"))

  def test_decode_url(self):
    url = "https://gist.github.com/mgp/92b50ae3e1b1b46eadab"
    parsed_url = self._parse_url(url)
    expected_dict = { "url": url }
    self.assertDictEqual(expected_dict, self.url_decoder.decode_url(url, parsed_url))

