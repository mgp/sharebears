class Token:
  """A token returned by the parse method."""

  TEXT = 1
  URL = 2
  HASH_TAG = 3

  def __init__(self, type, value):
    self.type = type
    self.value = value

  @staticmethod
  def text(value):
    """Returns a Token for the given text."""
    return Token(Token.TEXT, value)

  @staticmethod
  def url(value):
    """Returns a Token for the given URL."""
    return Token(Token.URL, value)

  @staticmethod
  def hash_tag(value):
    """Returns a Token for the given hash tag."""
    return Token(Token.HASH_TAG, value)


def _is_url(token_string):
  # Can use something more complicated like
  # https://github.com/django/django/blob/695956376ff09b0d6fd5c438f912b9eb05459145/django/core/validators.py#L68
  return token_string.startswith("http://") or token_string.startswith("https://")

def parse(string):
  """Parses the given string as a list of Token instances."""

  token_strings = string.strip().split()

  # Extract the tokens for hash tags.
  hash_tag_tokens = []
  for token_string in reversed(token_strings):
    if token_string.startswith("#"):
      hash_tag_token = Token.hash_tag(token_string[1:])
      hash_tag_tokens.append(hash_tag_token)
    else:
      break

  if hash_tag_tokens:
    hash_tag_tokens = list(reversed(hash_tag_tokens))
    # Extract text or URLs from the preceding tokens.
    token_strings = token_strings[:-len(hash_tag_tokens)]

  tokens = []
  def _add_token_for_words(words):
    tokens.append(Token.text(" ".join(words)))

  words = []
  for token_string in token_strings:
    if _is_url(token_string):
      if words:
        _add_token_for_words(words)
        words = []
      tokens.append(Token.url(token_string))
    else:
      words.append(token_string)
  if words:
    _add_token_for_words(words)

  return tokens + hash_tag_tokens

