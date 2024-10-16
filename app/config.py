import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CONGRESS_GOV_API_KEY = os.getenv('CONGRESS_GOV_API_KEY')
    OPEN_FEC_API_KEY = os.getenv('OPEN_FEC_API_KEY')
    OPEN_SECRETS_API_KEY = os.getenv('OPEN_SECRETS_API_KEY')
    PROPUBLICA_API_KEY = os.getenv('PROPUBLICA_API_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_TYPE = 'simple'

class DevelopmentConfig(Config):
    PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'postgresql://postgres:{PSQL_PASSWORD}@localhost/disclosure_campaign')

    CACHE_TYPE = 'simple'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

def get_config():
    env = os.getenv('FLASK_ENV', 'development')

    config = DevelopmentConfig

    if env == 'production':
        config = ProductionConfig

    return config
