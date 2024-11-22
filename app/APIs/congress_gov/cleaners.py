from datetime import datetime

def clean_bill_data(bill_data, key):
    cleaned_bills = []

    for bill in bill_data[key]:
        if 'title' in bill:
            cleaned_bills.append({
                'date:': bill['introducedDate'],
                'title': bill['title'],
                'url': bill['url'],
                'subject': bill['policyArea']['name']
            })

    return cleaned_bills

def get_current_title(terms):
    current_year = datetime.now().year
    latest_end_year = 0

    for term in terms:
        if 'endYear' in term:
            end_year = int(term['endYear'])
        else:
            end_year = current_year

        if end_year > latest_end_year:
            latest_end_year = end_year
            chamber = term['chamber']
            state = term['stateName']

    if int(current_year) <= latest_end_year:
        position = 'Senator' if chamber == 'Senate' else 'Representative'

        title = f'{position} from {state}'
    else:
        title = None

    return title

def add_member_data(politician, member_data):
    if 'depiction' in member_data:
        depiction = member_data['depiction']

        setattr(politician, 'depictionAttribution', depiction['attribution'])
        setattr(politician, 'depictionImageUrl', depiction['imageUrl'])

    if 'terms' in member_data:
        title = get_current_title(member_data['terms'])

        if title is not None:
            setattr(politician, 'currentTitle', title)

    politician.lastUpdated = datetime.now()
