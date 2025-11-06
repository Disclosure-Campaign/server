from flask import Blueprint, request, jsonify
from datetime import datetime

from .APIs.index import APIs
from .db.index import db_functions
from .helpers import use_cache

bp = Blueprint('api', __name__)

@bp.route('/request_searchable_entities')
def get_searchable_entities():
    result = use_cache([db_functions['request_searchable_entities'], None, 'searchable'])
    return result

@bp.route('/request_standard_data')
def request_standard_data():
    params = request.args.to_dict()
    result = False

    entity_type = params['entity_type']

    if entity_type == 'politician':
        result = use_cache([APIs['request_standard_politician_data'], params, entity_type])
    else:
        result = use_cache([APIs['request_standard_data'], params, entity_type])

    if result is None:
        result = jsonify({"error": "Failed to retrieve data from the API"}), 500
    else:
        result = jsonify(result)

    return result

@bp.route('/politician/financials/<fec_id>')
def get_politician_financials(fec_id):
    try:
        print(f"Fetching financial data for FEC ID: {fec_id}")
        result = use_cache([APIs['request_politician_data'], [fec_id, 'financials'], 'financials'])

        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), result.get('status', 500)

        return jsonify(result)

    except ValueError:
        return jsonify({"error": "Invalid year parameter"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/politician/geographic/<fec_id>')
def get_geographic_data(fec_id):
    try:
        year = request.args.get('year', datetime.now().year)
        params = {
            'type': 'geographic',
            'fec_id': fec_id,
            'year': int(year)
        }

        result = use_cache([APIs['request_politician_data'], [fec_id, ['geographic']], 'geographic'])

        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), result.get('status', 500)

        return jsonify(result)

    except ValueError:
        return jsonify({"error": "Invalid year parameter"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
