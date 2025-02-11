import re
import pandas as pd
from datetime import datetime

from app.db.session import get_session
from app.db.schemas.models import Politician
from app.db.custom.add_presidential_data import add_presidential_data
from app.helpers import split_name, construct_name, find_politician
from app.db.static_data.party_codes import party_codes

from app.helpers import update_politician

def update_politicians_from_txt(txt_path, session):
    print('Updating politicians from Opensecrets...')

    current_year = datetime.now().year

    with open(txt_path, 'r') as file:
        for line in file:
            row = line.strip().split('|')

            parts = split_name(row[1])
            fullName = construct_name(parts)

            if re.search(r'\d', fullName):
                print(f'Skipping row with name containing a number: {fullName}')
                continue

            electionYear = row[3]
            state = row[4]
            office = row[5]
            district = row[6]

            if district != '':
                district = str(int(district)).rjust(2, '0')

            column_values = {
                'fullName': fullName,
                'lastName': parts[0],
                'firstName': parts[1],
                'middleName': parts[2],
                'party': 'Unknown party' if row[2] not in party_codes else party_codes[row[2]],
                'candidateElectionYear': electionYear,
                'candidateOfficeState': state,
                'candidateOffice': office,
                'candidateOfficeDistrict': district,
                'candidateIncumbent': row[7],
                'candidateStatus': row[8],
                'candidateStreet1': row[10],
                'candidateStreet2': row[11],
                'candidateCity': row[12],
                'candidateState': row[13],
                'candidateZip': row[14] if row[14] != '' else 0,
                'lastUpdated': datetime.now()
            }

            fec_id = row[0]

            existing_politician = find_politician(session, {'fecId1': fec_id})

            if existing_politician:
                update_politician(existing_politician, column_values)
            elif int(electionYear) == current_year:
                column_values['fecId1'] = fec_id

                currentTitle = 'Candidate for '

                currentTitle += f'{state} Senator' if office == 'sen' else f'House Rep (District {district})'

                politician = Politician(**column_values)
                session.add(politician)

    session.commit()

    print('Opensecrets politicians update complete.')


def update_politicians_from_xls(xls_path, session):
    print('Updating politician id columns...')

    party_map = {
        'D': 'Democratic Party',
        'L': 'Libertarian Party',
        'R': 'Republican Party',
        'I': 'Independent'
    }

    # column_mapping = {
    #     'CID': 'opensecretsId',
    #     'CRPName': 'name',
    #     'Party': 'party',
    #     'DistIDRunFor': 'districtId',
    #     'FECCandID': 'fecId'
    # }

    sheets_to_process = ['Candidate Ids - 2024', 'Candidate Ids - 2022']
    start_row = 13
    start_col = 'B'

    df = pd.read_excel(xls_path, sheet_name=sheets_to_process, skiprows=start_row)

    # num_cols = df[sheets_to_process[0]].shape[1]
    # last_col_letter = chr(ord(start_col) + num_cols - 1)

    # usecols_range = f'{start_col}:{last_col_letter}'

    excel_data = pd.read_excel(xls_path, sheet_name=sheets_to_process, skiprows=start_row, usecols='B:F')

    for sheet_name, data in excel_data.items():
        print(f'Ingesting sheet: {sheet_name}')

        data = data.dropna(how='all')

        for index, row in data.iterrows():
            parts = split_name(row[1])
            fullName = construct_name(parts)

            opensecretsId = row[0]
            fecId = row[4]

            column_values = {
                'opensecretsId': opensecretsId,
                'fullName': fullName,
                'lastName': parts[0],
                'firstName': parts[1],
                'middleName': parts[2],
                'party': party_map.get(row[2], None),
                'fecId1': fecId
            }

            existing_politician = find_politician(
                session,
                {'fecId1': fecId, 'opensecretsId': opensecretsId}
            )

            if existing_politician:
                usable_data = {'opensecretsId': opensecretsId}

                update_politician(existing_politician, usable_data)
            # else:
            #     politician = Politician(**column_values)
            #     session.add(politician)

    session.commit()

    print('Politician id columns complete.')


def ingest():
    print('Starting ingest...')
    session = get_session()

    update_politicians_from_txt('app/db/bulk_data/cn.txt', session)
    update_politicians_from_xls('app/db/static_data/CRP_IDS.xls', session)
    add_presidential_data(session)

    session.close()
    print('Ingest complete.')

if __name__ == '__main__':
    ingest()