def clean_cand_contrib_data(data):
    cleaned_contributors = []

    contributors = data['response']['contributors']['contributor']

    for contributor in contributors:
        attributes = contributor['@attributes']

        cleaned_contributors.append({
            'org': attributes['org_name'],
            'total': int(attributes['total']),
            'indivs': int(attributes['indivs']),
            'pacs': int(attributes['pacs'])
        })

    return cleaned_contributors

def parse_member_profile(root):
    profile_data = {
        'name': root.find('member_profile').attrib.get('name', ''),
        'dataYear': root.find('member_profile').attrib.get('data_year', ''),
        'netLow': root.find('member_profile').attrib.get('net_low', ''),
        'netHigh': root.find('member_profile').attrib.get('net_high', ''),
        'assetLow': root.find('member_profile').attrib.get('asset_low', ''),
        'assetHigh': root.find('member_profile').attrib.get('asset_high', ''),
        'txLow': root.find('member_profile').attrib.get('tx_low', ''),
        'txHigh': root.find('member_profile').attrib.get('tx_high', ''),
        'updateTimestamp': root.find('member_profile').attrib.get('update_timestamp', ''),
    }

    assets = []

    for asset in root.findall('.//asset'):
        assets.append({
            'name': asset.attrib.get('name', ''),
            'holdings_low': asset.attrib.get('holdings_low', ''),
            'holdings_high': asset.attrib.get('holdings_high', ''),
            'industry': asset.attrib.get('industry', ''),
            'sector': asset.attrib.get('sector', ''),
            'subsidiary_of': asset.attrib.get('subsidiary_of', '')
        })

    transactions = []

    for transaction in root.findall('.//transaction'):
        transactions.append({
            'assetName': transaction.attrib.get('asset_name', ''),
            'txDate': transaction.attrib.get('tx_date', ''),
            'txAction': transaction.attrib.get('tx_action', ''),
            'valueLow': transaction.attrib.get('value_low', ''),
            'valueHigh': transaction.attrib.get('value_high', '')
        })

    positions = []

    for position in root.findall('.//position'):
        positions.append({
            'title': position.attrib.get('title', ''),
            'organization': position.attrib.get('organization', '')
        })

    profile_data['assets'] = assets
    profile_data['transactions'] = transactions
    profile_data['positions'] = positions

    return profile_data