from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
from server.models import db  # Import the database from models

app = Flask(__name__)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Set up the database migration commands with Flask's CLI
@app.cli.command('db init')
def init_db():
    """Initialize the migration repository."""
    from flask_migrate import init
    init()
    print("Database initialized!")

@app.cli.command('db migrate')
def migrate_db():
    """Create new migration."""
    from flask_migrate import migrate
    migrate()
    print("Database migration created!")

@app.cli.command('db upgrade')
def upgrade_db():
    """Apply the migration."""
    from flask_migrate import upgrade
    upgrade()
    print("Database upgraded!")

if __name__ == "__main__":
    # Do not run app in migration file
    pass
