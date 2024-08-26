from flask import jsonify
from sqlalchemy import asc
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.db.session import get_session
from app.db.schemas.models import Politician

from app.APIs.congress_gov.index import congress_gov_api
from app.APIs.open_fec.index import open_fec_api
from app.APIs.open_secrets.index import open_secrets_api

from app.helpers import find_politician


# api_map = {
#     'congress_gov': congress_gov_api,
#     'open_secrets': open_secrets_api
# }

relevant_years = [2022, 2024]

def request_standard_politician_data(params):
    session = get_session()

    id = params['id']

    data = None

    politician = find_politician(session, {'fecId': id})

    if politician:
        opensecrets_id = getattr(politician, 'opensecretsId')
        bioguide_id = getattr(politician, 'bioguideId')

        fec_ids = []

        for field in ['fecId1', 'fecId2', 'fecId3']:
            id = getattr(politician, field, None)

        if id:
            fec_ids.append(id)

        with ThreadPoolExecutor() as executor:
            info_futures = []

            def add_future(callback, params):
                info_futures.append(executor.submit(callback, params))

            if opensecrets_id:
                add_future(open_secrets_api['request_cand_contrib'], [opensecrets_id, 2024])
                add_future(open_secrets_api['request_mem_prof'], [opensecrets_id, 2016])

            if bioguide_id:
                add_future(congress_gov_api['request_bill_data'], [bioguide_id])

            info_groups = []

            for future in concurrent.futures.as_completed(info_futures):
                result = future.result()

                if isinstance(result, Exception):
                    print(f'Error occurred: {result}')
                else:
                    info_groups.append(result)

            data = info_groups

    return data

def request_searchable_entities():
    session = get_session()

    politicians = session.query(Politician).order_by(asc(Politician.lastName)).all()

    field_list = [
        'fullName',
        'lastName',
        'bioguideId',
        'fecId1',
        'fecId2',
        'fecId3'
    ]

    sortedPoliticians = []
    keyedPoliticians = {}

    for _politician in politicians:
        politician = {field: getattr(_politician, field) for field in field_list}
        politician['type'] = 'politician'

        sortedPoliticians.append(politician)
        keyedPoliticians[politician['fecId1']] = politician

    return jsonify({
        'sortedPoliticians': sortedPoliticians,
        'keyedPoliticians': keyedPoliticians
    })

APIs = {
    'request_standard_politician_data': request_standard_politician_data,
    'request_searchable_entities': request_searchable_entities
}