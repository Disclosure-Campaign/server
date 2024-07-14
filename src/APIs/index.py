from server.src.APIs.congress_gov.index import congress_gov_api

api_map = {
    'congress_gov': congress_gov_api
}

APIs = {}

def fetch_data(params):
    # data_type = params['data_type']
    # keywords = params['keywords']
    # key = params['key']

    api = api_map[params['api']]

    data = api['request_data'](params)

    return data


APIs['fetch_data'] = fetch_data