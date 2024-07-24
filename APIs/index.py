from app.APIs.congress_gov.index import congress_gov_api
from app.APIs.open_secrets.index import open_secrets_api

api_map = {
    'congress_gov': congress_gov_api,
    'open_secrets': open_secrets_api
}

def get_data(params):
    # data_type = params['data_type']
    # keywords = params['keywords']
    # key = params['key']

    api = api_map[params['api']]

    data = api['request_data'](params)

    return data

def request_searchable_entities():
    data = congress_gov_api['get_data']({
        'data_type': 'congressMembers'
    })

    return data

APIs = {
    'get_data': get_data,
    'request_searchable_entities': request_searchable_entities
}
