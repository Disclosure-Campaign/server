from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.cache import configure_cache
from app.config import get_config

migrate = Migrate()

db = SQLAlchemy()

origins = [
    'https://disclosurecampaign.org',
    'https://disclosure-campaign-site-6852e977de7d.herokuapp.com'
]

def create_app():
    print('Starting server...')

    server = Flask(__name__)
    CORS(server, resources={r'/*': {'origins': origins}})

    config_class = get_config()
    server.config.from_object(config_class())

    db.init_app(server)
    migrate.init_app(server, db)

    configure_cache(server)

    from app.routes import bp
    server.register_blueprint(bp)

    print('Server started.')

    return server
