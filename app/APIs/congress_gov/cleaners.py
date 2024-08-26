def clean_bill_data(bill_data, key):
    cleaned_bills = []

    print(bill_data.keys())

    for bill in bill_data[key]:
        if 'title' in bill:
            cleaned_bills.append({
                'date:': bill['introducedDate'],
                'title': bill['title'],
                'url': bill['url'],
                'subject': bill['policyArea']['name']
            })

    return cleaned_bills