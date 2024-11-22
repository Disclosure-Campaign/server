import requests
from datetime import datetime, timedelta

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.db.session import get_session
from app.config import get_config
from app.helpers import object_as_dict, find_politician
from .cleaners import clean_bill_data, add_member_data

config = get_config()

CONGRESS_GOV_API_KEY = config.CONGRESS_GOV_API_KEY

base_url = 'api.congress.gov/v3'

current_congress = 118

def request_bio_data(params):
    bioguide_id = params[0]
    id = params[1]

    session = get_session()

    politician = find_politician(session, {'fecId1': id})

    result = None

    last_updated_date = politician.lastUpdated
    is_recent = last_updated_date and (datetime.now() - last_updated_date) <= timedelta(days=7)

    has_attributes = True

    for attribute in ['currentTitle', 'depictionImageUrl']:
        if getattr(politician, attribute, None):
            has_attributes = False
            break

    if not has_attributes or not is_recent:
        url = f'https://{base_url}/member/{bioguide_id}?api_key={CONGRESS_GOV_API_KEY}'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                member_data = response.json()['member']

                add_member_data(politician, member_data)

                result = object_as_dict(politician)
            else:
                print(f'Error: bio API request failed with status code {response.status_code}')

        except requests.RequestException as e:
            print(f'Error: {e}')
    else:
        result = object_as_dict(politician)

    session.commit()
    session.close()

    return {'dataType': 'bio', 'data': result}

def request_bills_data(params):
    bioguideId = params[0]
    bill_group = params[1]

    url = f'https://{base_url}/member/'

    method = {
        'sponsoredLegislation': 'sponsored-legislation',
        'cosponsoredLegislation': 'cosponsored-legislation'
    }[bill_group];

    try:
        result = requests.get(f'{url}{bioguideId}/{method}?limit=250&api_key={CONGRESS_GOV_API_KEY}')

        data = result.json()

        cleaned_data = clean_bill_data(data, bill_group)
    except Exception as e:
        print(f'Error occurred while processing {method}: {e}')

        cleaned_data = None

    return {'data': cleaned_data}

def request_bill_data(params):
    congress, type, id = params['congress'], params['type'], params['id']

    url = f'https://{base_url}/bill/{congress}/{type}/{id}'

    with ThreadPoolExecutor() as executor:
        methods = ['', 'summaries']

        future_to_type = {
            executor.submit(requests.get, f'{url}/{method}?limit=250&api_key={CONGRESS_GOV_API_KEY}'): method
            for method in methods
        }

        bill_data = {}

        for index, future in enumerate(concurrent.futures.as_completed(future_to_type)):
            method = future_to_type[future]

            try:
                result = future.result().json()
                data_type = 'summaries' if method == 'summaries' else 'bill'
                key = data_type if method == 'summaries' else 'attributes'

                bill_data[key] = result[data_type]
            except Exception as e:
                print(f'Error occurred while processing {method}: {e}')

    return bill_data


congress_gov_api = {
    'request_bio_data': request_bio_data,
    'request_bills_data': request_bills_data,
    'request_bill_data': request_bill_data
}