import requests
from requests.auth import HTTPBasicAuth


class GitHubClientException(Exception):
  """An exception raised by a GitHubClient."""

  def __init__(self, reason):
    Exception.__init__(self)
    self.reason = reason

  def __str__(self):
    return str(self.reason)


class GitHubClient:
  """A client for communicating with the GitHub API."""

  _ROOT_ENDPOINT = "https://api.github.com"

  # TODO: Use a token for auth?
  def __init__(self, username, password):
    self.username = username
    self.password = password

  def _get_auth(self):
    # Unauthenticated requests are subject to more stringent rate limiting.
    # For details see https://developer.github.com/v3/#rate-limiting.
    if self.username and self.password:
      return HTTPBasicAuth(self.username, self.password)
    return None

  def _json_from_response_for_path(self, path):
    url = "%s/%s" % (_GitHubClient._ROOT_ENDPOINT, path)
    response = requests.get(url, auth=self._get_auth())
    if response.status_code == 200:
      return response.json()
    else:
      raise GitHubClientException("Status code was not 200 but was %s" % response.status_code)
  
  def get_repository(self, owner, repo):
    """Returns the JSON for the given repository by the given owner."""

    # See https://developer.github.com/v3/repos/#get
    path = "/repos/%s/%s" % (owner, repo)
    return self._json_from_response_for_path(path)

  def get_commit(self, owner, repo, sha):
    """Returns the JSON for the commit with the given SHA."""

    # See https://developer.github.com/v3/git/commits/#get-a-commit
    path = "/repos/%s/%s/git/commits/%s" % (owner, repo, sha)
    return self._json_from_response_for_path(path)

