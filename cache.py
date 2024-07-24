from flask_caching import Cache
from flask import current_app

cache = Cache()

def configure_cache(app):
    if app.config['CACHE_TYPE'] == 'redis':
        app.config['CACHE_REDIS_URL'] = app.config.get('CACHE_REDIS_URL')

    cache.init_app(app)

