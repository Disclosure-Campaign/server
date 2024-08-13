from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.cache import configure_cache
from app.config import get_config

migrate = Migrate()

db = SQLAlchemy()

def create_app():
    server = Flask(__name__)
    config_class = get_config()
    server.config.from_object(config_class())

    db.init_app(server)
    migrate.init_app(server, db)

    configure_cache(server)

    from app.routes import bp
    server.register_blueprint(bp)

    return server
