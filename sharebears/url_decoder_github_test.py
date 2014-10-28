import unittest

import url_decoder
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

  def test_item_for_rendering(self):
    owner_json = {"login": "login-value", "avatar_url": "avatar-url-value", "html_url": "html_url-value"}
    decoded_url = {
        "name": "name-value",
        "description": "description-value",
        "html_url": "html_url-value",
        "forks_count": 1,
        "stargazers_count": 2,
        "watchers_count": 3,
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2012-02-27T20:02:13Z",
        "owner": owner_json
    }
    item = self.url_decoder.item_for_rendering(decoded_url)

    self.assertEqual(decoded_url["name"], item.name)
    self.assertEqual(decoded_url["description"], item.description)
    self.assertEqual(decoded_url["html_url"], item.html_url)
    self.assertEqual(decoded_url["forks_count"], item.forks_count)
    self.assertEqual(decoded_url["stargazers_count"], item.stargazers_count)

    expected_datetime = url_decoder.to_datetime(decoded_url["created_at"])
    self.assertEqual(expected_datetime, item.created_at)
    expected_datetime = url_decoder.to_datetime(decoded_url["updated_at"])
    self.assertEqual(expected_datetime, item.updated_at)

    # Assert that the GitHubRepositoryOwnerItem instance is correct.
    owner = item.owner
    self.assertEqual(owner_json["login"], owner.login)
    self.assertEqual(owner_json["avatar_url"], owner.avatar_url)
    self.assertEqual(owner_json["html_url"], owner.html_url)


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

  def _make_user_json(self, name, email, date_string):
    return { "name": name, "email": email, "date": date_string }

  def _assert_user(self, user_json, user):
    self.assertEqual(user_json["name"], user.name)
    self.assertEqual(user_json["email"], user.email)
    expected_datetime = url_decoder.to_datetime(user_json["date"])
    self.assertEqual(expected_datetime, user.date)

  def test_item_for_rendering(self):
    author_json = self._make_user_json(
        "author_name", "author_email", "2010-04-10T14:10:01-07:00")
    committer_json = self._make_user_json(
        "committer_name", "committer_email", "2011-05-11T15:11:02-08:00")
    decoded_url = {
        "sha": "sha-value",
        "url": "url-value",
        "message": "message-value",
        "author": author_json,
        "committer": committer_json
    }
    item = self.url_decoder.item_for_rendering(decoded_url)

    self.assertEqual(decoded_url["sha"], item.sha)
    self.assertEqual(decoded_url["url"], item.url)
    self.assertEqual(decoded_url["message"], item.message)

    # Assert that the GitHubCommitUserItem instances are correct.
    self._assert_user(author_json, item.author)
    self._assert_user(committer_json, item.committer)


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

  def test_item_for_rendering(self):
    url = "https://gist.github.com/mgp/92b50ae3e1b1b46eadab"
    decoded_url = { "url": url }
    item = self.url_decoder.item_for_rendering(decoded_url)
    self.assertEqual(url, item.url)


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(GitHubRepositoryUrlDecoderTest))
  suite.addTest(unittest.makeSuite(GitHubCommitUrlDecoderTest))
  suite.addTest(unittest.makeSuite(GitHubGistUrlDecoderTest))
  return suite

