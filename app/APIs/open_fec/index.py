import time
import requests
from datetime import datetime
from app.config import get_config
from app.cache import cache
from app.helpers import object_as_dict

config = get_config()
OPEN_FEC_API_KEY = config.OPEN_FEC_API_KEY
base_url = 'api.open.fec.gov/v1'

data_type_map = {
    'congresscandidates': 'candidates',
    'financials': 'candidates',
    'geographic': 'schedules/schedule_a/by_state'
}

def validate_params(params):
    result = []

    if params:
        data_type = params.get('type', 'candidate')

        if not params.get('fec_id'):
            result.append("FEC ID is required")

        if data_type not in data_type_map:
            result.append(f"Invalid data type: {data_type}")

        year = params.get('year')
        if year:
            try:
                int(year)
            except ValueError:
                result.append(f"Invalid year format: {year}")

    return result

def process_response(response, data_type):
    result = None

    if response and response.status_code == 200:
        data = response.json()

        if data_type == 'financials':
            result = data.get('results', [])
            if result:
                result = result[0]
        elif data_type == 'geographic':
            result = {
                'contributions': data.get('results', []),
                'pagination': data.get('pagination', {})
            }
        else:
            result = data
    else:
        error_msg = f"API request failed with status {response.status_code}"

        if response.status_code == 429:
            error_msg = "Rate limit exceeded. Please try again later."
        elif response.status_code == 404:
            error_msg = "Resource not found"

        result = {'error': error_msg, 'status': response.status_code}

    return result

def request_fec_data(params):
    result = None
    errors = validate_params(params)

    if not errors:
        try:
            data_type = params.get('type', 'candidate')
            fec_id = params.get('fec_id')
            year = params.get('year')

            if data_type == 'financials':
                url = f'https://{base_url}/candidate/{fec_id}/totals'  # Note: singular 'candidate'
            elif data_type == 'geographic':
                url = f'https://{base_url}/schedules/schedule_a/by_state'
            else:
                endpoint = data_type_map.get(data_type)
                url = f'https://{base_url}/{endpoint}'

            request_params = {'api_key': OPEN_FEC_API_KEY}
            if year:
                if data_type == 'geographic':
                    request_params.update({
                        'candidate_id': fec_id,
                        'two_year_transaction_period': year,
                        'per_page': 100
                    })
                else:
                    request_params['election_year'] = year

            print(f"Making request to: {url} with params: {request_params}")  # Debug line
            response = requests.get(url, params=request_params)
            result = process_response(response, data_type)

        except requests.RequestException as e:
            result = {'error': str(e), 'status': 500}
    else:
        result = {'error': errors, 'status': 400}

    return result

open_fec_api = {
    'request_fec_data': request_fec_data
}