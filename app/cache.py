from flask_caching import Cache

cache = Cache()

def configure_cache(app):
    if app.config['CACHE_TYPE'] == 'redis':
        app.config['CACHE_REDIS_URL'] = app.config.get('CACHE_REDIS_URL')

    cache.init_app(app)

