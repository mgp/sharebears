import iso8601


class UrlDecoderException(Exception):
  """An exception raised by UrlDecoder."""

  def __init__(self, reason):
    Exception.__init__(self)
    self.reason = reason

  def __str__(self):
    return str(self.reason)


class RenderableItem:
  def __init__(self, type, item):
    self.type = type
    self.item = item


class UrlDecoder:
  @staticmethod
  def name():
    raise NotImplementedError

  @staticmethod
  def can_decode_url(url, parsed_url):
    raise NotImplementedError

  def decode_url(self, url, parsed_url):
    raise NotImplementedError

  def item_for_rendering(self, decoded_url):
    raise NotImplementedError


def filter_json(json, *keys):
  """Returns the given JSON but with only the given keys."""

  return {key: json[key] for key in keys if key in json}

def to_datetime(iso_8601_string):
  """Returns a datetime instance constructed from the given ISO 8601 string."""

  iso8601.parse_date(iso_8601_string)

