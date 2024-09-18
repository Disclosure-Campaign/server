from flask import Blueprint, request, jsonify

from .APIs.index import APIs
from .db.index import db_functions
from .helpers import use_cache

bp = Blueprint('api', __name__)

@bp.route('/request_searchable_entities')

def get_searchable_entities():
    result = db_functions['request_searchable_entities']()

    return result

@bp.route('/request_standard_data')

def request_standard_data():
    params = request.args.to_dict()
    result = False

    entity_type = params['entity_type']

    if entity_type == 'politician':
        result = use_cache(APIs['request_standard_politician_data'], params, entity_type)
    else:
        result = use_cache(APIs['request_standard_data'], params, entity_type)

    if not result:
        result = jsonify({"error": "Failed to retrieve data from the API"}), 500
    else:
        result = jsonify(result)

    return result