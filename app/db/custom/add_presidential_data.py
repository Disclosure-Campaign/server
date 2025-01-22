from app.db.schemas.models import Politician
from app.helpers import find_politician, update_politician

candidate_info_map = [
    {
        'lastName': 'Harris', 'firstName': 'Kamala', 'fullName': 'Kamala Harris', 'fecId1': 'P00009423',
        'opensecretsId': 'N00036915', 'bioguideId': 'H001075', 'party': 'Democratic Party',
        'currentTitle': 'Former Vice President',
        'website': 'https://kamalaharris.com',
        'contactForm': 'https://kamalaharris.com/connect/'

    },
    {
        'lastName': 'Trump', 'firstName': 'Donald', 'fullName': 'Donald J. Trump', 'fecId1': 'P80001571',
        'opensecretsId': 'N00023864', 'party': 'Republican Party',
        'depictionImageUrl': 'https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg',
        'depictionAttribution': 'https://en.m.wikipedia.org/wiki/File:Donald_Trump_official_portrait.jpg',
        'currentTitle': 'President',
        'website': 'https://www.donaldjtrump.com/',
        'contactForm': 'https://www.donaldjtrump.com/join'
    },
    {
        'lastName': 'Biden', 'firstName': 'Joseph', 'fullName': 'Joseph Biden', 'fecId1': 'P80000722',
        'opensecretsId': 'N00001669', 'bioguideId': 'B000444', 'party': 'Democratic Party',
        'currentTitle': 'Former President', 'nickname': 'Joe'
    }
]

shared_attributes = {
    'candidateElectionYear': 2024,
    'candidateOfficeState': 'US',
    'candidateOffice': 'P',
    'type': 'pres'
}

def add_presidential_data(session):
    print('Adding presidential data...')

    for attributes in candidate_info_map:
        pres_cand = find_politician(session, attributes)

        attributes.update(shared_attributes)

        if pres_cand is not None:
            update_politician(pres_cand, attributes)
        else:
            politician = Politician(**attributes)
            session.add(politician)

    session.commit()

    print('Added presidential data...')
