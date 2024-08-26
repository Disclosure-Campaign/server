import requests
from app.config import get_config

config = get_config()

PROPUBLICA_API_KEY = config.PROPUBLICA_API_KEY

data_type_map = {
    'congressMembers': 'member'
}

base_url = 'api.propublica.org/campaign-finance/v1'

def request_standard_data(params):
    result = None
    data_type = data_type_map[params['data_type']]
    name = params['name']
    year = params['year']

    url = f'https://{base_url}/{year}/{name}'

    # if data_type == 'member':
    #     if 'bio_id' in params:
    #         bio_id = params['bio_id']

    #         url += f'/{bio_id}'

    url += f'?api_key={PROPUBLICA_API_KEY}'

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



congress_gov_api = {
    'request_standard_data': request_standard_data
}