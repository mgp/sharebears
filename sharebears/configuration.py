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

  GOOGLE_APP_DOMAIN = "khanacademy.org"


def configure_app(app):
  # TODO: Use prod vs dev configuration based on environment variable.
  app.config.from_object(DevelopmentConfiguration)

  app.config.from_pyfile("../third_party_secrets.flask_cfg")

