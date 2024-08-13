from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.APIs.congress_gov.index import congress_gov_api
from app.APIs.open_fec.index import open_fec_api
from app.APIs.open_secrets.index import open_secrets_api

from ..helpers import stitch, combine_lists

api_map = {
    'congress_gov': congress_gov_api,
    'open_secrets': open_secrets_api
}

relevant_years = [2022, 2024]

def get_data(params):
    # data_type = params['data_type']
    # keywords = params['keywords']
    # key = params['key']

    api = api_map[params['api']]

    data = api['request_data'](params)

    return data

def request_searchable_entities():
    with ThreadPoolExecutor() as executor:
        candidates_futures = [
            executor.submit(open_fec_api['request_all_candidates'], year)
            for year in relevant_years
        ]

        congress_future = executor.submit(congress_gov_api['request_all_congress_members'])

        candidates = []

        for future in concurrent.futures.as_completed(candidates_futures):
            candidates = combine_lists(candidates, future.result(), 'candidate_id')

        congress_members = congress_future.result()

    all_politicians = stitch(candidates, congress_members)

    keyedPoliticians = {member['id']: member for member in all_politicians}
    sortedPoliticians = sorted(all_politicians, key=lambda person: person['lastName'].lower())

    result = {
        'keyedPoliticians': keyedPoliticians,
        'sortedPoliticians': sortedPoliticians
    }

    return result

APIs = {
    'get_data': get_data,
    'request_searchable_entities': request_searchable_entities
}