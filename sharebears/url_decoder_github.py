import re

from url_decoder import UrlDecoder, UrlDecoderException, filter_json


class _GitHubUrlDecoder(UrlDecoder):
  def is_decodeable_url(self, url, parsed_url):
    if not parsed_url.netloc.startswith("github."):
      return False
    return True


class GitHubRepositoryUrlDecoder(_GitHubUrlDecoder):
  """Renders a GitHub repository."""

  _PATH_REGEX = re.compile("^/(?P<owner>\w+)/(?P<repo>\w+)$")

  def __init__(self, github_client):
    self.github_client = github_client

  def name(self):
    return "github-repository"

  def _match_parsed_url(self, parsed_url):
    return GitHubRepositoryUrlDecoder._PATH_REGEX.match(parsed_url.path)

  def is_decodeable_url(self, url, parsed_url):
    if not _GitHubUrlDecoder.is_decodeable_url(self, url, parsed_url):
      return False
    elif not self._match_parsed_url(parsed_url):
      return False
    return True

  def _filter_json(self, json):
    """Filters the JSON from https://developer.github.com/v3/repos/#get"""

    # Filter the repository owner.
    owner_json = json["owner"]
    filtered_owner_json = filter_json(owner_json, "login", "avatar_url", "html_url")

    # Filter the repository.
    filtered_json = filter_json(json,
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

  def name(self):
    return "github-commit"

  def _match_parsed_url(self, parsed_url):
    return GitHubCommitUrlDecoder._PATH_REGEX.match(parsed_url.path)

  def is_decodeable_url(self, url, parsed_url):
    if not _GitHubUrlDecoder.is_decodeable_url(self, url, parsed_url):
      return False
    elif not self._match_parsed_url(parsed_url):
      return False
    return True

  def _filter_json(self, json):
    """Filters the JSON from https://developer.github.com/v3/git/commits/#get-a-commit"""

    return filter_json(json,
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

  def name(self):
    return "github-gist"

  def is_decodeable_url(self, url, parsed_url):
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
