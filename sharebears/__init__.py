from flask import Flask

app = Flask(__name__.split('.')[0])

# Import the configuration.
import configuration
app.config.from_object(configuration.from_environment())

# Remove some whitespace from the HTML.
app.jinja_env.trim_blocks = app.config['JINJA_TRIM_BLOCKS']

# Set up the database.
import db
import db_util
import db_schema
engine = db_util.init_db(app.config["DATABASE_NAME"], app.config["DATABASE_URI"])
db_schema.create_all_tables(engine) 

# Register the handlers.
import views

