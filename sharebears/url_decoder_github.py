import re

import url_decoder
from url_decoder import UrlDecoder, UrlDecoderException


class _GitHubUrlDecoder(UrlDecoder):
  @staticmethod
  def can_decode_url(url, parsed_url):
    if not parsed_url.netloc.startswith("github."):
      return False
    return True


class GitHubRepositoryOwnerItem:
  """The owner in a GitHubRepositoryItem."""

  def __init__(self, decoded_owner):
    self.login = decoded_owner["login"]
    self.avatar_url = decoded_owner["avatar_url"]
    self.html_url = decoded_owner["html_url"]


class GitHubRepositoryItem:
  """A GitHub repository for a RenderableItem."""

  def __init__(self, decoded_url):
    self.name = decoded_url["name"]
    self.description = decoded_url["description"]
    self.html_url = decoded_url["html_url"]
    self.language = decoded_url["language"]

    self.owner = GitHubRepositoryOwnerItem(decoded_url["owner"])


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
  def can_decode_url(url, parsed_url):
    if not _GitHubUrlDecoder.can_decode_url(url, parsed_url):
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
        "language")

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

  def item_for_rendering(self, decoded_url):
    return GitHubRepositoryItem(decoded_url)



class GitHubCommitUserItem:
  """A user in a GitHubCommitItem."""

  def __init__(self, decoded_user):
    self.name = decoded_user["name"]
    self.email = decoded_user["email"]
    self.date = url_decoder.to_datetime(decoded_user["date"])


class GitHubCommitItem:
  """A GitHub commit for a RenderableItem."""

  def __init__(self, decoded_url):
    self.sha = decoded_url["sha"]
    self.url = decoded_url["url"]
    self.message = decoded_url["message"]

    self.author = GitHubCommitUserItem(decoded_url["author"])
    self.committer = GitHubCommitUserItem(decoded_url["committer"])


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
  def can_decode_url(url, parsed_url):
    if not _GitHubUrlDecoder.can_decode_url(url, parsed_url):
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

  def item_for_rendering(self, decoded_url):
    return GitHubCommitItem(decoded_url)



class GitHubGistItem:
  """A GitHub Gist for a RenderableItem."""

  def __init__(self, decoded_url):
    self.url = decoded_url["url"]


class GitHubGistUrlDecoder(UrlDecoder):
  """Embeds a Gist."""

  _PATH_REGEX = re.compile("^/\w+/\w+$")

  @staticmethod
  def name():
    return "github-gist"

  @staticmethod
  def can_decode_url(url, parsed_url):
    if not parsed_url.netloc.startswith("gist.github."):
      return False
    elif not GitHubGistUrlDecoder._PATH_REGEX.match(parsed_url.path):
      return False
    return True

  def decode_url(self, url, parsed_url):
    # Use an embedded Gist.
    return { "url": url }

  def item_for_rendering(self, decoded_url):
    return GitHubGistItem(decoded_url)

