from flask import Flask
from server.config import get_config
from server.cache import configure_cache

def create_server():
    server = Flask(__name__)
    config = get_config()
    server.config.from_object(config)

    configure_cache(server)

    from server.routes import bp
    server.register_blueprint(bp)

    return server
