import requests
from server.config import get_config

config = get_config()

CONGRESS_GOV_API_KEY = config.CONGRESS_GOV_API_KEY

data_type_map = {
    'congressMembers': 'member'
}

base_url = "api.congress.gov/v3"

def request_data(params):
    result = None
    data_type = data_type_map[params['data_type']]

    url = f'https://{base_url}/{data_type}'

    if data_type == 'member':
        if 'bio_id' in params:
            url += f'/{params['bio_id']}'

    url += '?api_key={CONGRESS_GOV_API_KEY}'

    try:
        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
        else:
            print(f"Error: API request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error: {e}")

        result = e

    return result

congress_gov_api = {
    'request_data': request_data
}