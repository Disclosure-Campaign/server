import requests
from server.config import get_config

config = get_config()

OPEN_SECRETS_API_KEY = config.OPEN_SECRETS_API_KEY

data_type_map = {
    'congressMembers': 'getLegislators'
}

base_url = 'www.opensecrets.org/api'

def request_searchable_entities():
    result = None

    url = f'https://{base_url}/?method=getLegislators&id=NJ&apikey={OPEN_SECRETS_API_KEY}'

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

open_secrets_api = {
    'request_searchable_entities': request_searchable_entities
}