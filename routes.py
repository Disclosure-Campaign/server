from flask import Blueprint, request, jsonify, current_app
import hashlib
import json

from server.cache import cache
from server.APIs.index import APIs

# app = Flask(__name__)
# cors = CORS(app)

def generate_cache_key(params, route):
    sorted_params = json.dumps(params, sort_keys=True)

    return f'{route}-{hashlib.md5(sorted_params.encode('utf-8')).hexdigest()}'

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

    cache_key = generate_cache_key(params, 'get_searchable_entities')
    cache_data = check_cache(cache_key)

    if cache_data is not None:
        result = cache_data
    else:
        result = APIs['request_searchable_entities']()

        cache.set(cache_key, result, timeout=60*60*24)

    print(result)

    return result

@bp.route('/get_data')

def request_specific_data():
    params = request.args.to_dict()

    result = APIs['get_data'](params)

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to retrieve data from the API"}), 500