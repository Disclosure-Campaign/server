import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.schemas.models import Politician

database_url = 'PROD_DATABASE_URL' if os.getenv('FLASK_ENV') == 'production' else 'DEV_DATABASE_URL'
DATABASE_URL = os.getenv(database_url)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

politicians = session.query(Politician).limit(5).all()

print("\nFirst 5 politicians and their FEC IDs:")
for pol in politicians:
    print(f"{pol.fullName}: {pol.fecId1}")