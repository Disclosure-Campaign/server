import requests
from app.config import get_config

config = get_config()

PROPUBLICA_API_KEY = config.PROPUBLICA_API_KEY

data_type_map = {
    'congressMembers': 'member'
}

base_url = 'api.propublica.org/campaign-finance/v1'

def request_politician_data(params):
    result = None
    name = params['name']
    year = params['year']

    url = f'https://{base_url}/{year}/{name}?api_key={PROPUBLICA_API_KEY}'

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
    'request_politician_data': request_politician_data
}