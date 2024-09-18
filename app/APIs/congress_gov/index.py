import requests
from datetime import datetime, timedelta

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.config import get_config
from app.helpers import object_as_dict
from .cleaners import clean_bill_data, add_member_data

config = get_config()

CONGRESS_GOV_API_KEY = config.CONGRESS_GOV_API_KEY

base_url = 'api.congress.gov/v3'

current_congress = 118

def request_bio_data(params):
    bioguide_id = params[0]
    politician = params[1]
    session = params[2]

    last_updated_date = politician.lastUpdated
    is_recent = last_updated_date and (datetime.now() - last_updated_date) <= timedelta(days=7)

    if not getattr(politician, 'currentTitle', None) or not is_recent:
        url = f'https://{base_url}/member/{bioguide_id}?api_key={CONGRESS_GOV_API_KEY}'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                member_data = response.json()['member']

                add_member_data(politician, member_data)

                session.commit()
            else:
                print(f'Error: API request failed with status code {response.status_code}')
        except requests.RequestException as e:
            print(f'Error: {e}')

    return {'dataType': 'bio', 'data': object_as_dict(politician)}

def request_bills_data(params):
    bioguideId = params[0]

    url = f'https://{base_url}/member/'

    with ThreadPoolExecutor() as executor:
        methods = ['sponsored-legislation', 'cosponsored-legislation']

        future_to_type = {
            executor.submit(requests.get, f'{url}{bioguideId}/{method}?limit=250&api_key={CONGRESS_GOV_API_KEY}'): method
            for method in methods
        }

        bill_data = {}

        for index, future in enumerate(concurrent.futures.as_completed(future_to_type)):
            method = future_to_type[future]

            try:
                result = future.result().json()
                data_type = 'sponsoredLegislation' if method == 'sponsored-legislation' else 'cosponsoredLegislation'

                cleaned_data = clean_bill_data(result, data_type)
                bill_data[data_type] = cleaned_data
            except Exception as e:
                print(f'Error occurred while processing {method}: {e}')

    return {'dataType': 'billData', 'data': bill_data}

def request_bill_data(params):
    congress, type, id = params['congress'], params['type'], params['id']

    url = f'https://{base_url}/bill/{congress}/{type}/{id}'

    with ThreadPoolExecutor() as executor:
        methods = ['', '/summaries', ]

        future_to_type = {
            executor.submit(requests.get, f'{url}/{method}?limit=250&api_key={CONGRESS_GOV_API_KEY}'): method
            for method in methods
        }

        bill_data = {}

        for index, future in enumerate(concurrent.futures.as_completed(future_to_type)):
            method = future_to_type[future]

            try:
                result = future.result().json()
                data_type = 'summaries' if method == '/summaries' else 'bill'

                bill_data[data_type] = result[data_type]
            except Exception as e:
                print(f'Error occurred while processing {method}: {e}')

    return bill_data


congress_gov_api = {
    'request_bio_data': request_bio_data,
    'request_bills_data': request_bills_data,
    'request_bill_data': request_bill_data
}