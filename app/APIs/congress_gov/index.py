import requests
from app.config import get_config

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from .cleaners import clean_bill_data

config = get_config()

CONGRESS_GOV_API_KEY = config.CONGRESS_GOV_API_KEY

data_type_map = {
    'congressMembers': 'member'
}

base_url = 'api.congress.gov/v3'

current_congress = 118

def request_bill_data(params):
    bioguideId = params[0]

    url = f'https://{base_url}/member/'

    with ThreadPoolExecutor() as executor:
        bill_futures = [
            executor.submit(requests.get, bill_url)
            for bill_url in [
                f'{url}{bioguideId}/{method}?limit=250&api_key={CONGRESS_GOV_API_KEY}'
                for method in ['sponsored-legislation', 'cosponsored-legislation']
            ]
        ]

        bill_data = []
        types = ['sponsoredLegislation', 'cosponsoredLegislation']

        for index, future in enumerate(concurrent.futures.as_completed(bill_futures)):
            result = future.result().json()

            if isinstance(result, Exception):
                print(f'Error occurred: {result}')
            else:
                data = clean_bill_data(result, types[index])

                bill_data.append(data)

    return {'billData': bill_data}

congress_gov_api = {
    'request_bill_data': request_bill_data
}