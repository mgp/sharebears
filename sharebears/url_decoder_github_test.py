from url_decoder_test import UrlDecoderTestCase
from url_decoder_github import GitHubRepositoryUrlDecoder, GitHubCommitUrlDecoder, GitHubGistUrlDecoder


class _GitHubTestClient:
  def __init__(self):
    self.get_repository_args = []
    self.get_commit_args = []

  def _get_repository_json(self):
    owner_json = { "login": "mgp" }
    return { "owner": owner_json, "name": "repo-name" }

  def get_repository(self, *pargs):
    self.get_repository_args.append(pargs)
    return self._get_repository_json()

  def _get_commit_json(self):
    return { "sha": "a8b7818", "message": "Initial commit" }

  def get_commit(self, *pargs):
    self.get_commit_args.append(pargs)
    return self._get_commit_json()


class GitHubRepositoryUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.test_client = _GitHubTestClient()
    self.url_decoder = GitHubRepositoryUrlDecoder(self.test_client)

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
    url = "https://github.com/mgp/sharebears"
    parsed_url = self._parse_url(url)
    json = self.url_decoder.decode_url(url, parsed_url)
    self.assertDictEqual(json, self.test_client._get_repository_json())

    self.assertEqual(0, len(self.test_client.get_commit_args))
    self.assertEqual(1, len(self.test_client.get_repository_args))
    owner, repo = self.test_client.get_repository_args[0]
    self.assertEqual("mgp", owner)
    self.assertEqual("sharebears", repo)


class GitHubCommitUrlDecoderTest(UrlDecoderTestCase):
  def setUp(self):
    UrlDecoderTestCase.setUp(self)
    self.test_client = _GitHubTestClient()
    self.url_decoder = GitHubCommitUrlDecoder(self.test_client)

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
    url = "https://github.com/mgp/sharebears/commit/a8b7818"
    parsed_url = self._parse_url(url)
    json = self.url_decoder.decode_url(url, parsed_url)
    self.assertDictEqual(json, self.test_client._get_commit_json())

    self.assertEqual(0, len(self.test_client.get_repository_args))
    self.assertEqual(1, len(self.test_client.get_commit_args))
    owner, repo, sha = self.test_client.get_commit_args[0]
    self.assertEqual("mgp", owner)
    self.assertEqual("sharebears", repo)
    self.assertEqual("a8b7818", sha)


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

