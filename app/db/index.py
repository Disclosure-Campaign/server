from flask import jsonify
from sqlalchemy import asc

from app.db.schemas.models import Politician
from app.db.session import get_session

def request_searchable_entities():
    session = get_session()

    politicians = session.query(Politician).order_by(asc(Politician.lastName)).all()

    field_list = [
        'fullName',
        'lastName',
        'bioguideId',
        'fecId1',
        'fecId2',
        'fecId3',
        'party'
    ]

    sortedPoliticians = []
    keyedPoliticians = {}

    for _politician in politicians:
        politician = {field: getattr(_politician, field) for field in field_list}
        politician['type'] = 'politician'

        sortedPoliticians.append(politician)
        keyedPoliticians[politician['fecId1']] = politician

    return jsonify({
        'sortedPoliticians': sortedPoliticians,
        'keyedPoliticians': keyedPoliticians
    })

db_functions = {
    'request_searchable_entities': request_searchable_entities
}