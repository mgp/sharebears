import urlparse

import album_item
import parser
from parser import Token
import paragraph_item
from renderable_item import RenderableItem


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
    self._decoders = decoders
    self._decoders_by_name = {decoder.name(): decoder for decoder in decoders}


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

  def _decoder_for_url(self, url, parsed_url):
    """Returns the decoder that matches the given URL, if any."""
    for decoder in self._decoders:
      if decoder.can_decode_url(url, parsed_url):
        return decoder
    return None


  def process(self, string):
    """Returns a ProcessedPost instance from the given string."""

    parser_tokens = parser.parse(string)

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
        url = token_value
        parsed_url = urlparse.urlparse(url)
        token_decoder = self._decoder_for_url(url, parsed_url)
        if token_decoder == None:
          data.append(PostProcessor._make_data_element(PostProcessor._URL_TYPE, token_value))
        else:
          decoder_type = PostProcessor._type_for_decoder(token_decoder)
          decoded_url = token_decoder.decode_url(url, parsed_url)
          data.append(PostProcessor._make_data_element(decoder_type, decoded_url))
      else:
        raise Exception("Unknown token type: %s" % token_type)

    return ProcessedPost(data, hash_tags)


  def _renderable_item_for_data_element(self, data_element):
    element_type = data_element["type"]
    element_value = data_element["value"]
    if element_type == PostProcessor._TEXT_TYPE:
      return RenderableItem.for_text(element_value)
    elif element_type == PostProcessor._URL_TYPE:
      return RenderableItem.for_url(element_value)
    else:
      decoder_name = PostProcessor._name_for_decoder_type(element_type)
      decoder = self._decoders_by_name[decoder_name]
      item = decoder.item_for_rendering(element_value)
      return RenderableItem.for_renderer(decoder_name, item)


  _RENDERABLE_ITEM_TRANSFORMERS = [
      album_item.insert_albums,
      paragraph_item.insert_paragraphs,
  ]

  def renderable_items(self, post_data):
    """Returns a sequence of RenderableItems from the given processed post."""

    renderable_items = [self._renderable_item_for_data_element(element) for element in post_data]
    for item_transformer in PostProcessor._RENDERABLE_ITEM_TRANSFORMERS:
      renderable_items = item_transformer(renderable_items)
    return renderable_items

