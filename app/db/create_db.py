import os
import pandas as pd
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schemas.models import Base, Politician

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    Base.metadata.create_all(engine)

def insert_data(data):
    for _, row in data.iterrows():
        column_values = {
            'firstName': row['first_name'],
            'middleName': row['middle_name'],
            'lastName': row['last_name'],
            'fullName': row['full_name'],
            'bioguideId': row['bioguide_id'],
            'state': row['state'],
            'district': row['district'],
            'party': row['party'],
            'birthday': row['birthday'],
            'type': row['type'],
            'website': row['url'],
            'phone': row['phone'],
            'contactForm': row['contact_form'],
            'twitter': row['twitter'],
            'facebook': row['facebook']
        }

        if row['fec_ids'] != '':
            fec_ids = row['fec_ids'].split(',')

            for index, id in enumerate(fec_ids, 1):
                column_values[f'candidateId{index}'] = id
        else:
            column_values['candidateId1'] = row['bioguide_id']

        politician = Politician(**column_values)

        session.add(politician)

    session.commit()

numeric_columns = ['district']
date_columns = ['birthday']

def main():
    create_tables()

    df = pd.read_csv('app/db/static_data/legislators_current.csv')

    fill_values = {}

    for column in df.columns:
        if column in numeric_columns:
            fill_values[column] = 0
        elif column in date_columns:
            fill_values[column] = pd.Timestamp('1970-01-01')
        else:
            fill_values[column] = ''

    df.fillna(value=fill_values, inplace=True)

    insert_data(df)

if __name__ == '__main__':
    main()
