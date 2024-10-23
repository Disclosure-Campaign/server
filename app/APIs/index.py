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
    result = use_cache(get_politician_data, params, 'politician')

    return result

def get_politician_data(params):
    id = params[0]
    only_bio = params[1] == 'true'

    session = get_session()

    data = None

    politician = find_politician(session, {'fecId1': id})

    if politician:
        opensecrets_id = getattr(politician, 'opensecretsId')
        bioguide_id = getattr(politician, 'bioguideId')

        fec_ids = []

        for field in ['fecId1', 'fecId2', 'fecId3']:
            _id = getattr(politician, field, None)

            if _id is not None:
                fec_ids.append(_id)

        with ThreadPoolExecutor() as executor:
            info_futures = []

            def add_future(callback, params):
                info_futures.append(executor.submit(callback, params))

            if bioguide_id is not None:
                add_future(congress_gov_api['request_bio_data'], [bioguide_id, politician])

                if not only_bio:
                    add_future(congress_gov_api['request_bills_data'], [bioguide_id])
            else:
                add_future(db_functions['get_bio_from_db'], [session, politician])

            if (opensecrets_id is not None) and not only_bio:
                add_future(open_secrets_api['request_cand_contrib'], [opensecrets_id, 2024])
                add_future(open_secrets_api['request_mem_prof'], [opensecrets_id, 2016])

            info_groups = []

            for future in concurrent.futures.as_completed(info_futures):
                result = future.result()

                if isinstance(result, Exception):
                    print(f'Error occurred: {result}')
                elif result['data'] is None:
                    data_type = result['dataType']

                    print(f'{data_type} data unavailable')
                else:
                    info_groups.append(result)

            data = {}

            for group in info_groups:
                if group['dataType'] == 'billData':
                    data['sponsoredLegislation'] = group['data']['sponsoredLegislation']
                    data['cosponsoredLegislation'] = group['data']['cosponsoredLegislation']
                else:
                    data[group['dataType']] = group['data']

    session.commit()
    session.close()

    return {id: data}

def request_standard_politician_data(params):
    ids = params['ids'].split('-')
    only_bio = params['onlyBio']

    all_data = {}

    with ThreadPoolExecutor() as executor:
        info_futures = []

        for id in ids:
            info_futures.append(executor.submit(cached_get_politician_data, [id, only_bio]))

        for future in concurrent.futures.as_completed(info_futures):
            data = future.result()

            for id in ids:
                if id in data:
                    all_data[id] = data[id]

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