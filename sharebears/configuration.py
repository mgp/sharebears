class Configuration:
  """Configuration used in all environments."""
  JINJA_TRIM_BLOCKS = True


class DevelopmentConfiguration(Configuration):
  """Configuration used in a local development environment."""
  DEBUG = True
  TESTING = False
  DATABASE_NAME = "sqlite"
  DATABASE_URI = "sqlite://"
  SECRET_KEY = 'secret_key'


def from_environment():
  # TODO: Return prod vs dev configuration based on environment variable.
  return DevelopmentConfiguration

