class Configuration:
  """Configuration used in all environments."""
  JINJA_TRIM_BLOCKS = True


class DevelopmentConfiguration(Configuration):
  """Configuration used in a local development environment."""
  DEBUG = True
  TESTING = False
  SECRET_KEY = 'secret_key'

  DATABASE_NAME = "sqlite"
  DATABASE_URI = "sqlite://"

  GOOGLE_CLIENT_ID = "908613102039-379d2f5q3u6odqk0dfi200d2ha6hh768.apps.googleusercontent.com"
  GOOGLE_CLIENT_SECRET = "IrhXmcoqgu3X6FlKV8nN3tov"
  GOOGLE_APP_DOMAIN = "khanacademy.org"


def from_environment():
  # TODO: Return prod vs dev configuration based on environment variable.
  return DevelopmentConfiguration

