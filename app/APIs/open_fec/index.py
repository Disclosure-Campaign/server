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
    data_type = data_type_map[params['data_type']]
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

def request_all_candidates(election_year):
    all_candidates_fetched = False
    error = False
    candidates = []
    result = None
    wait_time = 0.1

    original_url = f'https://{base_url}/candidates?election_year={election_year}&is_active_candidate=true&per_page=100&'
    current_url = original_url

    while not (all_candidates_fetched or error):
        try:
            response = requests.get(f'{current_url}api_key={OPEN_FEC_API_KEY}')

            if response.status_code == 200:
                data = response.json()

                candidates = candidates + data['results']
                count = len(candidates)

                if ('count' in data['pagination']) and (data['pagination']['count'] > count):
                    next_page = data['pagination']['page'] + 1

                    current_url = original_url + f'page={next_page}&'
                else:
                    all_candidates_fetched = True

                    result = candidates
            elif response.status_code == 429:
                time.sleep(wait_time)

                print(wait_time)

                wait_time *= 2

                if wait_time > 1000:
                    break
            else:
                print(f'Error: API request failed with status code {response.status_code}')

                break
        except requests.RequestException as error:
            print(f'Error: {error}')

            result = error

    return result

open_fec_api = {
    'request_politician_data': request_politician_data,
    'request_all_candidates': request_all_candidates
}