import os
from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.cache import configure_cache
from app.config import get_config

load_dotenv()

migrate = Migrate()

db = SQLAlchemy()

origins = [
    'disclosurecampaign.org',
    'www.disclosurecampaign.org',
    'https://disclosurecampaign.org',
    'https://www.disclosurecampaign.org',
    os.getenv('HEROKU_SITE_URL'),
    os.getenv('CLOUDFLARE_NAMESERVER_1'),
    os.getenv('CLOUDFLARE_NAMESERVER_2'),
    # 'http://localhost:3000'
]

def create_app():
    print('Starting server...')

    server = Flask(__name__)
    CORS(server, resources={r'/*': {'origins': '*'}})

    config_class = get_config()
    server.config.from_object(config_class())

    db.init_app(server)
    migrate.init_app(server, db)

    configure_cache(server)

    from app.routes import bp
    server.register_blueprint(bp)

    print('Server started.')

    return server
