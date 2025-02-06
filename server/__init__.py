from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app():
    """Create and configure the Flask app."""
    
    # Initialize Flask app
    app = Flask(__name__)

    # Configure app with settings
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Import models (only if necessary here to avoid circular imports)
    from .models import Restaurant, Pizza, RestaurantPizza

    # Register Blueprints or API resources
    from .app import api
    api.init_app(app)

    # Ensure the database is created
    with app.app_context():
        db.create_all()

    return app
