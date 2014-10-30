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

  @staticmethod
  def for_oauth_token(oauth_token):
    """Returns a GitHubClient instance that authenticates using the given OAuth token.
    
    See https://developer.github.com/v3/auth/#via-oauth-tokens for details.
    """
    def _oauth_strategy():
      return HTTPBasicAuth(oauth_token, "x-oauth-basic")
    return GitHubClient(_oauth_strategy)


  def __init__(self, auth_strategy=None):
    self.auth_strategy = auth_strategy

  def _get_auth(self):
    # Unauthenticated requests are subject to more stringent rate limiting.
    # See https://developer.github.com/v3/#rate-limiting for details.
    if self.auth_strategy:
      return self.auth_strategy()
    return None

  def _json_from_response_for_path(self, path):
    url = "%s/%s" % (GitHubClient._ROOT_ENDPOINT, path)
    response = requests.get(url, auth=self._get_auth())
    if response.status_code == 200:
      return response.json()
    else:
      raise GitHubClientException("Status code was not 200 but was %s" % response.status_code)
  
  def get_repository(self, owner, repo):
    """Returns the JSON for the given repository by the given owner."""

    # See https://developer.github.com/v3/repos/#get
    path = "repos/%s/%s" % (owner, repo)
    return self._json_from_response_for_path(path)

  def get_commit(self, owner, repo, sha):
    """Returns the JSON for the commit with the given SHA."""

    # See https://developer.github.com/v3/git/commits/#get-a-commit
    path = "repos/%s/%s/git/commits/%s" % (owner, repo, sha)
    return self._json_from_response_for_path(path)

