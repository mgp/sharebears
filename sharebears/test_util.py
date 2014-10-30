class TestDecoder:
  def __init__(self, name, matched_url_prefix):
    self._name = name
    self._matched_url_prefix = matched_url_prefix

  def name(self):
    return self._name

  def can_decode_url(self, url, parsed_url):
    return url.startswith(self._matched_url_prefix)

  def decode_url(self, url, parsed_url):
    return "decoded-%s" % url

  def item_for_rendering(self, decoded_url):
    return "rendered-%s" % decoded_url

