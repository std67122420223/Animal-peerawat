import os
from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

 
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"sslmode": "require"}
    }

    db.init_app(app)

    from .routes import main_bp
    from .users.routes import users_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix="/users")

    return app