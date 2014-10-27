class UrlDecoderException(Exception):
  """An exception raised by UrlDecoder."""

  def __init__(self, reason):
    Exception.__init__(self)
    self.reason = reason

  def __str__(self):
    return str(self.reason)


class UrlDecoder:
  @staticmethod
  def name():
    raise NotImplementedError

  @staticmethod
  def is_decodeable_url(url, parsed_url):
    raise NotImplementedError

  def decode_url(self, url, parsed_url):
    raise NotImplementedError

  def render_decoded_url(self, decoded_url):
    raise NotImplementedError


def filter_json(json, *keys):
  """Returns the given JSON but with only the given keys."""

  return {key: json[key] for key in keys if key in json}

