from flask import Blueprint, request, jsonify, current_app
import hashlib
import json

from app.cache import cache
from app.APIs.index import APIs

ignore_cache = True

def generate_cache_key(params, route):
    sorted_params = json.dumps(params, sort_keys=True)

    hashed_params = hashlib.md5(sorted_params.encode('utf-8')).hexdigest()

    return f'{route}-{hashed_params}'

def check_cache(cache_key):
    result = None
    cached_data = cache.get(cache_key)

    if cached_data:
        current_app.logger.info(f'Cache hit for key: {cache_key}')

        result = jsonify(cached_data)

    return result

bp = Blueprint('api', __name__)

@bp.route('/get_searchable_entities')

def get_searchable_entities():
    params = request.args.to_dict()

    result = APIs['request_searchable_entities']()

    # cache_key = generate_cache_key(params, 'get_searchable_entities')
    # cache_data = check_cache(cache_key)

    # if (cache_data is not None) and (ignore_cache is False):
    #     print('using cache')

    #     result = cache_data
    # else:
    #     result = APIs['request_searchable_entities']()

    #     cache.set(cache_key, result, timeout=60*60*24)

    return result

@bp.route('/request_standard_data')

def request_standard_data():
    params = request.args.to_dict()
    data_type = params['type']

    if data_type == 'politician':
        result = APIs['request_standard_politician_data'](params)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to retrieve data from the API"}), 500
