import time
import requests
from app.config import get_config

config = get_config()

OPEN_FEC_API_KEY = config.OPEN_FEC_API_KEY

data_type_map = {
    'congresscandidates': 'candidate'
}

base_url = 'api.open.fec.gov/v1'

def request_politician_data(params):
    result = None
    name = params['name']
    year = params['year']

    url = f'https://{base_url}/{year}/{name}'

    # if data_type == 'candidate':
    #     if 'bio_id' in params:
    #         bio_id = params['bio_id']

    #         url += f'/{bio_id}'

    url += f'?api_key={OPEN_FEC_API_KEY}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

        result = e

    return result

open_fec_api = {
    'request_politician_data': request_politician_data,
    'request_all_candidates': request_all_candidates
}