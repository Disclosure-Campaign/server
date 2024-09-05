from flask import Blueprint, request, jsonify

from .APIs.index import APIs
from .helpers import use_cache

bp = Blueprint('api', __name__)

@bp.route('/get_searchable_entities')

def get_searchable_entities():
    result = APIs['request_searchable_entities']()

    return result

@bp.route('/request_standard_data')

def request_standard_data():
    params = request.args.to_dict()
    data_type = params['type']

    result = False

    if data_type == 'politician':
        result = use_cache(APIs['request_standard_politician_data'], params, 'rspd')

    if not result:
        result = jsonify({"error": "Failed to retrieve data from the API"}), 500
    else:
        result = jsonify(result)

    return result