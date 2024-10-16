import requests
import xml.etree.ElementTree as ET

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from app.config import get_config
from .cleaners import clean_cand_contrib_data, parse_member_profile
from app.helpers import fuzzy_match

generic = [
    'group',
    'fund',
    'llc',
    'ventures',
    'trading',
    'industry',
    'coalition',
    'campaign'
]

config = get_config()

OPEN_SECRETS_API_KEY = config.OPEN_SECRETS_API_KEY

base_url = 'www.opensecrets.org/api'

def request_legislators(state):
    result = None

    url = f'https://{base_url}/?method=getLegislators&output=json&id={state}&apikey={OPEN_SECRETS_API_KEY}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
        else:
            print(f'Error: legislator API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

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
            print(f'Error: contrib API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

    return {'dataType': 'candContrib', 'data': result}

def request_mem_prof(params):
    id = params[0]
    year = params[1]

    url = f'https://{base_url}/?method=memPFDprofile&output=xml&cid={id}&year={year}&apikey={OPEN_SECRETS_API_KEY}'

    result = None

    try:
        response = requests.get(url)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            result = parse_member_profile(root)
        else:
            print(f'Error: mem prof API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

    return {'dataType': 'memProf', 'data': result}

def request_org_data(params):
    org_slug = params['org_slug']

    id = find_org_id(org_slug)

    url = f'https://{base_url}/?method=orgSummary&id={id}&output=json&apikey={OPEN_SECRETS_API_KEY}'

    result = None

    try:
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()['response']['organization']['@attributes']
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.RequestException as e:
        print(f'Error: {e}')

    return {'org': result}

def find_org_id(org_slug):
    org_name = org_slug.replace('-', ' ')

    result = None

    with ThreadPoolExecutor() as executor:
        org_name_parts = org_slug.split('-')
        cleaned_org_name_parts = [part for part in org_name_parts if part.lower() not in generic]
        org_futures = []
        possible_orgs = []

        for org_name_part in cleaned_org_name_parts:
            org_futures.append(executor.submit(
                requests.get,
                f'https://{base_url}/?method=getOrgs&org={org_name_part}&output=json&apikey={OPEN_SECRETS_API_KEY}'
            ))

        for future in concurrent.futures.as_completed(org_futures):
            result = future.result()

            if isinstance(result, Exception):
                print(f'Error occurred: {result}')
            else:
                for _org in result.json()['response']['organization']:
                    org = _org['@attributes']

                    if org['orgname'].lower() == org_name:
                        return org['orgid']
                    else:
                        org['score'] = fuzzy_match(org['orgname'], org_name)

                        possible_orgs.append(org)

    best_score = 0
    best_org = possible_orgs[0]

    for org in possible_orgs[1:]:
        score = org['score']

        if score > best_score:
            best_org = org
            best_score = score

    return best_org['orgid']

open_secrets_api = {
    'request_legislators': request_legislators,
    'request_cand_contrib': request_cand_contrib,
    'request_mem_prof': request_mem_prof,
    'request_org_data': request_org_data
}