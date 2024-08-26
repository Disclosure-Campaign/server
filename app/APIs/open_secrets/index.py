import requests
import xml.etree.ElementTree as ET

from app.config import get_config
from .cleaners import clean_cand_contrib_data

config = get_config()

OPEN_SECRETS_API_KEY = config.OPEN_SECRETS_API_KEY

data_type_map = {
    'congressMembers': 'getLegislators'
}

base_url = 'www.opensecrets.org/api'

def request_legislators(state):
    result = None

    url = f'https://{base_url}/?method=getLegislators&output=json&id={state}&apikey={OPEN_SECRETS_API_KEY}'

    try:
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

        result = e

    return result

def request_cand_contrib(params):
    id = params[0]
    year = params[1]

    result = None

    url = f'https://{base_url}/?method=candContrib&output=json&cid={id}&cycle={year}&apikey={OPEN_SECRETS_API_KEY}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            raw_data = response.json()

            result = clean_cand_contrib_data(raw_data)
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

        result = e

    return {'cand_contrib': result}

def request_mem_prof(params):
    id = params[0]
    year = params[1]

    url = f'https://{base_url}/?method=memPFDprofile&output=xml&cid={id}&year={year}&apikey={OPEN_SECRETS_API_KEY}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            member_data = parse_member_profile(root)
            result = parse_member_profile(root)
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

        result = e

    return {'mem_prof': result}

open_secrets_api = {
    'request_legislators': request_legislators,
    'request_cand_contrib': request_cand_contrib,
    'request_mem_prof': request_mem_prof
}

def parse_member_profile(root):
    member_profile = root.find('member_profile')

    member_data = {
        'data_year': member_profile.get('data_year'),
        'net_low': member_profile.get('net_low'),
        'net_high': member_profile.get('net_high'),
        'positions_held_count': member_profile.get('positions_held_count'),
        'asset_count': member_profile.get('asset_count'),
        'asset_low': member_profile.get('asset_low'),
        'asset_high': member_profile.get('asset_high'),
        'transaction_count': member_profile.get('transaction_count'),
        'tx_low': member_profile.get('tx_low'),
        'tx_high': member_profile.get('tx_high'),
        'source': member_profile.get('source'),
        'origin': member_profile.get('origin'),
        'update_timestamp': member_profile.get('update_timestamp')
    }

    return member_data