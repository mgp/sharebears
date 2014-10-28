import urlparse

from parser import Parser, Token


class ProcessedPost:
  def __init__(self, data, hash_tags):
    self.data = data
    self.hash_tags = hash_tags


class PostProcessor:
  """Processes a post so that it is suitable for storage or rendering."""

  _TEXT_TYPE = "text"
  _URL_TYPE = "url"
  _DECODED_URL_TYPE_PREFIX = "%s-" % _URL_TYPE

  def __init__(self, decoders):
    self._parser = Parser(decoders)


  @staticmethod
  def _make_data_element(element_type, value):
    """Creates an element for the data list of ProcessedPost."""
    return {"type": element_type, "value": value}

  @staticmethod
  def _type_for_decoder(decoder):
    """Returns the element type for a URL with the given decoder."""
    return "%s%s" % (PostProcessor._DECODED_URL_TYPE_PREFIX, decoder.name())

  @staticmethod
  def _name_for_decoder_type(decoder_type):
    """Returns the name of the decoder for the URL with the given type."""
    if decoder_type.startswith(PostProcessor._DECODED_URL_TYPE_PREFIX):
      return decoder_type[len(PostProcessor._DECODED_URL_TYPE_PREFIX):]
    raise Exception("Unknown decoder type: %s" % decoder_type)


  def process(self, string):
    """Returns a ProcessedPost instance from the given string."""

    parser_tokens = self._parser.parse(string)

    data = []
    hash_tags = []
    for parser_token in parser_tokens:
      token_type = parser_token.type
      token_value = parser_token.value

      if token_type == Token.TEXT:
        data.append(PostProcessor._make_data_element(PostProcessor._TEXT_TYPE, token_value))
      elif token_type == Token.HASH_TAG:
        if token_value not in hash_tags:
          hash_tags.append(token_value)
      elif token_type == Token.URL:
        token_decoder = parser_token.decoder
        if token_decoder == None:
          data.append(PostProcessor._make_data_element(PostProcessor._URL_TYPE, token_value))
        else:
          url = token_value
          parsed_url = urlparse.urlparse(url)
          decoded_url = token_decoder.decode_url(url, parsed_url)
          decoder_type = PostProcessor._type_for_decoder(token_decoder)
          data.append(PostProcessor._make_data_element(decoder_type, decoded_url))
      else:
        raise Exception("Unknown token type: %s" % token_type)

    return ProcessedPost(data, hash_tags)


  def renderable_items(self, post_data):
    """Returns a sequence of RenderableItems from the given processed post."""

    for data_element in post_data:
      element_type = data_element["type"]
      if element_type == PostProcessor._TEXT_TYPE:
        pass
      elif element_type == PostProcessor._URL_TYPE:
        pass
      elif element_type == "TODO":
        pass

