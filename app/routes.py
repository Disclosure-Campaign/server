from flask import Blueprint, request, jsonify

from .APIs.index import APIs
from .db.index import db_functions
from .helpers import use_cache

bp = Blueprint('api', __name__)

@bp.route('/request_searchable_entities')

def get_searchable_entities():
    result = db_functions['request_searchable_entities']()

    return result

@bp.route('/request_politician_data')

def request_politician_data():
    params = request.args.to_dict()
    result = False

    result = use_cache(APIs['request_standard_politician_data'], params, 'rspd')

    if not result:
        result = jsonify({"error": "Failed to retrieve data from the API"}), 500
    else:
        result = jsonify(result)

    return result

@bp.route('/request_bill_data')

def request_bill_data():
    params = request.args.to_dict()
    result = False

    params['data_type'] = 'bill'

    result = use_cache(APIs['request_standard_data'], params, 'bill')

    if not result:
        result = jsonify({"error": "Failed to retrieve data from the API"}), 500
    else:
        result = jsonify(result)

    return result