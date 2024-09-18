from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.db.session import get_session

from app.APIs.congress_gov.index import congress_gov_api
from app.APIs.open_fec.index import open_fec_api
from app.APIs.open_secrets.index import open_secrets_api

from app.helpers import find_politician

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

            if bioguide_id:
                add_future(congress_gov_api['request_bio_data'], [bioguide_id, politician, session])
                add_future(congress_gov_api['request_bills_data'], [bioguide_id])

            if opensecrets_id:
                add_future(open_secrets_api['request_cand_contrib'], [opensecrets_id, 2024])
                add_future(open_secrets_api['request_mem_prof'], [opensecrets_id, 2016])

            info_groups = []

            for future in concurrent.futures.as_completed(info_futures):
                result = future.result()

                if isinstance(result, Exception):
                    print(f'Error occurred: {result}')
                else:
                    info_groups.append(result)

            data = {}

            for group in info_groups:
                if group['dataType'] == 'billData':
                    data['sponsoredLegislation'] = group['data']['sponsoredLegislation']
                    data['cosponsoredLegislation'] = group['data']['cosponsoredLegislation']
                else:
                    data[group['dataType']] = group['data']

    return data

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