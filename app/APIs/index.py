from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.db.session import get_session
from app.db.index import db_functions

from app.APIs.congress_gov.index import congress_gov_api
from app.APIs.open_fec.index import open_fec_api
from app.APIs.open_secrets.index import open_secrets_api

from app.helpers import find_politician, use_cache

relevant_years = [2022, 2024]

def cached_get_politician_data(params):
    result = use_cache([get_politician_data, params, 'politician'])

    return result

def get_politician_data(params):
    fec_id = params[0]
    dataGroup = params[1]

    data = {}
    session = get_session()
    politician = find_politician(session, {'fecId1': fec_id})

    if politician:
        opensecrets_id = getattr(politician, 'opensecretsId')
        bioguide_id = getattr(politician, 'bioguideId')

        fec_ids = []

        for field in ['fecId1', 'fecId2', 'fecId3']:
            _id = getattr(politician, field, None)

            if _id is not None:
                fec_ids.append(_id)

        if dataGroup == 'bio':
            # add bio from db idea
            result = use_cache([congress_gov_api['request_bio_data'], [bioguide_id, fec_id], 'bio'])
        elif dataGroup == 'sponsoredLegislation':
            result = use_cache([congress_gov_api['request_bills_data'], [bioguide_id, dataGroup], 'bills'])
        elif dataGroup == 'cosponsoredLegislation':
            result = use_cache([congress_gov_api['request_bills_data'], [bioguide_id, dataGroup], 'bills'])
        elif dataGroup == 'candContrib':
            result = use_cache([open_secrets_api['request_cand_contrib'], [opensecrets_id, 2024], 'cand_contrib'])
        elif dataGroup == 'memProf':
            result = use_cache([open_secrets_api['request_mem_prof'], [opensecrets_id, 2016], 'mem_prof'])

        if isinstance(result, Exception):
            print(f'Error occurred: {result}')
        elif result['data'] is None:
            print(f'{dataGroup} data unavailable')

            data = {dataGroup: 'unavailable'}
        else:
            data = {dataGroup: result['data']}

    session.commit()
    session.close()

    return {fec_id: data}

def request_standard_politician_data(params):
    fec_ids = params['ids'].split('-')
    dataGroup = params['dataGroup']

    all_data = {}

    with ThreadPoolExecutor() as executor:
        info_futures = []

        for fec_id in fec_ids:
            info_futures.append(executor.submit(cached_get_politician_data, [fec_id, dataGroup]))

        for future in concurrent.futures.as_completed(info_futures):
            data = future.result()

            for fec_id in fec_ids:
                if fec_id in data:
                    all_data[fec_id] = data[fec_id]

    return all_data

def request_standard_data(params):
    data = None

    if params['entity_type'] == 'bill':
        data = congress_gov_api['request_bill_data'](params)
    elif params['entity_type'] == 'org':
        data = open_secrets_api['request_org_data'](params)

    return data

APIs = {
    'request_standard_politician_data': request_standard_politician_data,
    'request_standard_data': request_standard_data
}