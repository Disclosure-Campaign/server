import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

database_url = 'PROD_DATABASE_URL' if os.getenv('FLASK_ENV') == 'production' else 'DEV_DATABASE_URL'

DATABASE_URL = os.getenv(database_url)

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

def get_session():
    return Session()

