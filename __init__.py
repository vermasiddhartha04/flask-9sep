from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Import and initialize roles inside app context
    with app.app_context():
        from .models import initialize_roles
        db.create_all()
        initialize_roles()

    return app
