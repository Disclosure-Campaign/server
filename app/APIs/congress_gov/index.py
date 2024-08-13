import requests
from app.config import get_config

config = get_config()

CONGRESS_GOV_API_KEY = config.CONGRESS_GOV_API_KEY

data_type_map = {
    'congressMembers': 'member'
}

base_url = 'api.congress.gov/v3'

current_congress = 118

def request_data(params):
    result = None
    data_type = data_type_map[params['data_type']]

    url = f'https://{base_url}/{data_type}'

    if data_type == 'member':
        if 'bio_id' in params:
            bio_id = params['bio_id']

            url += f'/{bio_id}'

    url += f'?api_key={CONGRESS_GOV_API_KEY}'

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

def request_all_congress_members():
    all_members_fetched = False
    error = False
    members = []
    result = None

    current_url = f'https://{base_url}/member/congress/{current_congress}?limit=250&'

    while not (all_members_fetched or error):
        try:
            response = requests.get(f'{current_url}api_key={CONGRESS_GOV_API_KEY}')

            if response.status_code == 200:
                data = response.json()

                members = members + data['members']

                if 'next' in data['pagination']:
                    current_url = data['pagination']['next'].replace('limit=20', 'limit=250') + '&'
                else:
                    all_members_fetched = True

                    result = members
            else:
                print(f'Error: API request failed with status code {response.status_code}')

                break
        except requests.RequestException as error:
            print(f'Error: {error}')

            result = error

    return result

congress_gov_api = {
    'request_data': request_data,
    'request_all_congress_members': request_all_congress_members
}