import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    CONGRESS_GOV_API_KEY = os.getenv('CONGRESS_GOV_API_KEY')
    OPEN_SECRETS_API_KEY = os.getenv('OPEN_SECRETS_API_KEY')
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_TYPE = 'simple'

class DevelopmentConfig(Config):
    CACHE_TYPE = 'simple'

class ProductionConfig(Config):
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

def get_config():
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        return ProductionConfig

    return DevelopmentConfig
