import re

import url_decoder
from url_decoder import UrlDecoder, UrlDecoderException


class _GitHubUrlDecoder(UrlDecoder):
  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not parsed_url.netloc.startswith("github."):
      return False
    return True


class GitHubRepositoryUrlDecoder(_GitHubUrlDecoder):
  """Renders a GitHub repository."""

  _PATH_REGEX = re.compile("^/(?P<owner>\w+)/(?P<repo>\w+)$")

  def __init__(self, github_client):
    self.github_client = github_client

  @staticmethod
  def name():
    return "github-repository"

  @staticmethod
  def _match_parsed_url(parsed_url):
    return GitHubRepositoryUrlDecoder._PATH_REGEX.match(parsed_url.path)

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not _GitHubUrlDecoder.is_decodeable_url(url, parsed_url):
      return False
    elif not GitHubRepositoryUrlDecoder._match_parsed_url(parsed_url):
      return False
    return True

  def _filter_json(self, json):
    """Filters the JSON from https://developer.github.com/v3/repos/#get"""

    # Filter the repository owner.
    owner_json = json["owner"]
    filtered_owner_json = url_decoder.filter_json(owner_json,
        "login", "avatar_url", "html_url")

    # Filter the repository.
    filtered_json = url_decoder.filter_json(json,
        "name",
        "description",
        "html_url",
        "forks_count",
        "stargazers_count",
        "watchers_count",
        "created_at",
        "updated_at")

    filtered_json["owner"] = filtered_owner_json
    return filtered_json

  def decode_url(self, url, parsed_url):
    match = self._match_parsed_url(parsed_url)
    if not match:
      raise UrlDecoderException("URL is not decodeable: %s" % parsed_url)
    owner = match.group("owner")
    repo = match.group("repo")
    json = self.github_client.get_repository(owner, repo)
    return self._filter_json(json)

  def render_decoded_url(self, decoded_url):
    # TODO
    pass


class GitHubCommitUrlDecoder(_GitHubUrlDecoder):
  """Renders a commit belonging to a GitHub repository."""

  _PATH_REGEX = re.compile("^/(?P<owner>\w+)/(?P<repo>\w+)/commit/(?P<sha>\w+)$")

  def __init__(self, github_client):
    self.github_client = github_client

  @staticmethod
  def name():
    return "github-commit"

  @staticmethod
  def _match_parsed_url(parsed_url):
    return GitHubCommitUrlDecoder._PATH_REGEX.match(parsed_url.path)

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not _GitHubUrlDecoder.is_decodeable_url(url, parsed_url):
      return False
    elif not GitHubCommitUrlDecoder._match_parsed_url(parsed_url):
      return False
    return True

  def _filter_json(self, json):
    """Filters the JSON from https://developer.github.com/v3/git/commits/#get-a-commit"""

    return url_decoder.filter_json(json,
        "sha",
        "url",
        "author",
        "committer",
        "message")

  def decode_url(self, url, parsed_url):
    match = self._match_parsed_url(parsed_url)
    if not match:
      raise UrlDecoderException("URL is not decodeable: %s" % parsed_url)
    owner = match.group("owner")
    repo = match.group("repo")
    sha = match.group("sha")
    json = self.github_client.get_commit(owner, repo, sha)
    return self._filter_json(json)

  def render_decoded_url(self, decoded_url):
    # TODO
    pass


class GitHubGistUrlDecoder(UrlDecoder):
  """Embeds a Gist."""

  _PATH_REGEX = re.compile("^/\w+/\w+$")

  @staticmethod
  def name():
    return "github-gist"

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    if not parsed_url.netloc.startswith("gist.github."):
      return False
    elif not GitHubGistUrlDecoder._PATH_REGEX.match(parsed_url.path):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded Gist.
    return { "url": url }

  def render_decoded_url(self, decoded_url):
    # TODO
    pass

