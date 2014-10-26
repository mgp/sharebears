class Token:
  """A token returned by the Parser."""

  TEXT = 1
  URL = 2
  HASH_TAG = 3

  def __init__(self, type, value):
    self.type = type
    self.value = value

  @staticmethod
  def text(value):
    """Returns a Token for the given text."""
    return Token(TEXT, value)

  @staticmethod
  def hash_tag(value):
    """Returns a Token for the given hash tag."""
    return Token(HASH_TAG, value)


class UrlToken(Token):
  """A token containing a URL, with its decoder if one is available."""

  def __init__(self, url, decoder):
    Token.__init__(self, url)
    self.decoder = decoder


class Parser:
  def __init__(self, decoders):
    self.decoders = decoders

  @staticmethod
  def _is_url(token_string):
    # TODO
    pass

  def decoder_for_url(self, url):
    """Returns the decoder that matches the given URL, if any."""
    for decoder in decoders:
      if decoder.matches_url(url):
        return decoder
    return None

  def parse(self, string):
    """Parses the given string as a list of Token instances."""

    token_strings = string.trim().split()

    # Extract the tokens for hash tags.
    hash_tag_tokens = []
    for token_string in reversed(token_strings):
      if token_string.startswith("#"):
        hash_tag_token = Token.hash_tag(token_string[1:])
        hash_tag_tokens.append(hash_tag_token)
      else:
        break

    # Extract text or URLs from the preceding tokens.
    token_strings = [:-len(hash_tag_tokens)]
    tokens = []
    for token_string in token_strings:
      token = None
      if Parser._is_url(token_string):
        decoder = self.decoder_for_url(token_string)
        token = UrlToken(token_string, decoder)
      else:
        token = Token.text(token_string)
      tokens.append(token)

    return tokens + hash_tag_tokens

