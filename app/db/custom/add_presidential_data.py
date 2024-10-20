from app.helpers import find_politician

candidate_info_map = [
    {
        'name': 'Harris', 'fecId': 'P00009423',
        'opensecretsId': 'N00036915', 'bioguideId': 'H001075',
        'currentTitle': 'Vice President & candidate for President',
        'website': 'https://kamalaharris.com',
        'contactForm': 'https://kamalaharris.com/contact-us/', 'twitter': 'VP',
        'facebook': 'KamalaHarris'

    },
    {
        'name': 'Trump', 'fecId': 'P80001571',
        'opensecretsId': 'N00023864',
        'depictionImageUrl': 'https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg',
        'depictionAttribution': 'https://en.m.wikipedia.org/wiki/File:Donald_Trump_official_portrait.jpg',
        'currentTitle': 'Former President & candidate for President',
        'website': 'https://www.donaldjtrump.com/',
        'contactForm': 'https://www.donaldjtrump.com/join', 'twitter': 'realDonaldTrump',
        'facebook': 'DonaldTrump'
    },
    {
        'name': 'Biden', 'fecId': 'P80000722',
        'opensecretsId': 'N00001669', 'bioguideId': 'B000444',
        'currentTitle': 'President',
        'website': 'https://www.whitehouse.gov/administration/president-biden',
        'contactForm': 'https://www.whitehouse.gov/contact', 'twitter': 'potus',
        'facebook': 'POTUS/s'
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
        pres_cand = find_politician(session, {'fecId1': attributes['fecId']})

        attributes.update(shared_attributes)

        for attribute, value in attributes.items():
            setattr(pres_cand, attribute, value)

    session.commit()

    print('Added presidential data...')




