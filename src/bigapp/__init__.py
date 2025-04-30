import os
from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv

from .models import db, User

load_dotenv()


def create_app():
    app = Flask(__name__, static_folder="../../frontend/build")

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-for-testing")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)

    # Set up Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .app import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)

    # Serve React app
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + "/" + path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app
