from flask import jsonify
from sqlalchemy import asc

from app.db.schemas.models import Politician, Zip
from app.db.session import get_session
from app.helpers import find_politician, object_as_dict

def request_searchable_entities():
    session = get_session()

    politicians = session.query(Politician).order_by(asc(Politician.lastName)).all()

    politician_field_list = [
        'fullName',
        'lastName',
        'nickname',
        'fecId1',
        'bioguideId',
        'opensecretsId',
        'currentTitle',
        'party',
        'candidateOfficeState',
        'candidateOfficeDistrict',
        'depictionImageUrl',
        'website',
        'contactForm',
        'twitter',
        'facebook'
    ]

    sortedPoliticians = []
    keyedPoliticians = {}

    for _politician in politicians:
        politician = {field: getattr(_politician, field) for field in politician_field_list}
        politician['type'] = 'politician'

        sortedPoliticians.append(politician)
        keyedPoliticians[politician['fecId1']] = politician

    zips = session.query(Zip).all()

    zip_field_list = ['zip', 'district', 'state']

    zipList = []
    keyedZips = {}

    for _zip in zips:
        zip = {field: getattr(_zip, field) for field in zip_field_list}

        zip_code = zip['zip']

        if zip_code in keyedZips:
            keyedZips[zip_code].append(zip)
        else:
            zipList.append(zip)
            keyedZips[zip_code] = [zip]

    session.commit()
    session.close()

    return jsonify({
        'sortedPoliticians': sortedPoliticians,
        'keyedPoliticians': keyedPoliticians,
        'zipList': zipList,
        'keyedZips': keyedZips
    })

def get_bio_from_db(params):
    session = params[0]
    fec_id = params[1]

    bio_data = find_politician(session, {'fecId1': fec_id})

    return {'dataType': 'bio', 'data': object_as_dict(bio_data)}

db_functions = {
    'request_searchable_entities': request_searchable_entities,
    'get_bio_from_db': get_bio_from_db
}