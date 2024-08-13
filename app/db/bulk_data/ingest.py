from datetime import datetime
from sqlalchemy import or_

from app.db.session import get_session
from app.db.schemas.models import Politician
from app.helpers import normalize_name
from app.db.static_data.party_codes import party_codes

def update_politicians_from_txt(txt_path):
    session = get_session()

    with open(txt_path, 'r') as file:
        for line in file:
            row = line.strip().split('|')

            column_values = {
                'fullName': normalize_name(row[1]),
                'party': 'Unknown party' if row[2] not in party_codes else party_codes[row[2]],
                'candidateElectionYear': row[3],
                'candidateOfficeState': row[4],
                'candidateOffice': row[5],
                'candidateOfficeDistrict': row[6],
                'candidateIncumbent': row[7],
                'candidateStatus': row[8],
                'candidateStreet1': row[10],
                'candidateStreet2': row[11],
                'candidateCity': row[12],
                'candidateState': row[13],
                'candidateZip': row[14] if row[14] != '' else 0,
                'lastUpdated': datetime.now(),
            }

            candidate_id = row[0]

            existing_politician = session.query(Politician).filter(
                or_(
                    Politician.candidateId1 == candidate_id,
                    Politician.candidateId2 == candidate_id,
                    Politician.candidateId3 == candidate_id
                )
            ).first()

            if existing_politician:
                for key, value in column_values.items():
                    if value != '':
                        setattr(existing_politician, key, value)
            else:
                column_values['candidateId1'] = candidate_id

                politician = Politician(**column_values)
                session.add(politician)

    session.commit()

    print('Database update complete.')

update_politicians_from_txt('app/db/bulk_data/cn.txt')