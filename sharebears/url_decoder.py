class UrlDecoder:
  def name(self):
    raise NotImplementedError

  def is_decodeable_url(self, url, parsed_url):
    raise NotImplementedError

  def decode_url(self, url, parsed_url)
    raise NotImplementedError

  def render_decoded_url(self, decoded_url):
    raise NotImplementedError

