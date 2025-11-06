from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.db.session import get_session
from app.db.index import db_functions

from app.APIs.congress_gov.index import congress_gov_api
from app.APIs.open_fec.index import open_fec_api
from app.APIs.open_secrets.index import open_secrets_api

from app.helpers import find_politician, use_cache

relevant_years = [2022, 2024]

def cached_request_politician_data(params):
    result = use_cache([request_politician_data, params, 'politician'])

    return result

def request_financial_data(fec_id):
    result = {}

    for year in relevant_years:
        financial_params = {
            'type': 'financials',
            'fec_id': fec_id,
            'year': year
        }

        year_data = open_fec_api['request_fec_data'](financial_params)

        if year_data:
            result[year] = year_data

    return result

def request_geographic_data(fec_id):
    result = {}

    for year in relevant_years:
        geo_params = {
            'type': 'geographic',
            'fec_id': fec_id,
            'year': year
        }
        year_data = open_fec_api['request_fec_data'](geo_params)
        if year_data:
            result[year] = year_data

    return result

def request_politician_data(params):
    fec_id = params[0]
    dataGroup = params[1]
    result = None

    session = get_session()
    politician = find_politician(session, {'fecId1': fec_id})

    if politician:
        bioguide_id = getattr(politician, 'bioguideId')
        data = {}

        if dataGroup == 'financials':
            financial_data = request_financial_data(fec_id)

            if financial_data:
                data = {'financials': financial_data}

        elif dataGroup == 'geographic':
            geographic_data = request_geographic_data(fec_id)

            if geographic_data:
                data = {'geographic': geographic_data}

        elif dataGroup == 'bio':
            cached_data = use_cache([congress_gov_api['request_bio_data'], [bioguide_id, fec_id], 'bio'])
            if cached_data and not isinstance(cached_data, Exception):
                data = {'bio': cached_data.get('data', 'unavailable')}

        elif dataGroup in ['sponsoredLegislation', 'cosponsoredLegislation']:
            cached_data = use_cache([congress_gov_api['request_bills_data'], [bioguide_id, dataGroup], 'bills'])
            if cached_data and not isinstance(cached_data, Exception):
                data = {dataGroup: cached_data.get('data', 'unavailable')}

        if data:
            result = {fec_id: data}

    session.commit()
    session.close()

    return result

def request_standard_politician_data(params):
    fec_ids = params['ids'].split('-')
    dataGroup = params['dataGroup']

    all_data = {}

    with ThreadPoolExecutor() as executor:
        info_futures = []

        for fec_id in fec_ids:
            info_futures.append(executor.submit(cached_request_politician_data, [fec_id, dataGroup]))

        for future in concurrent.futures.as_completed(info_futures):
            data = future.result()

            for fec_id in fec_ids:
                if data is not None and fec_id in data:
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
    'request_standard_data': request_standard_data,
    'request_politician_data': request_politician_data
}