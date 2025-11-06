# api.congress.gov/#/member/member_list

congress_fields = [
  {'key': 'bioguideId', 'data_type': 'shortString'},
  {'key': 'depictionAttribution', 'data_type': 'extraLongString'},
  {'key': 'depictionImageUrl', 'data_type': 'longString'},
  {'key': 'district', 'data_type': 'integer'},
  {'key': 'firstName', 'data_type': 'string'},
  {'key': 'lastName', 'data_type': 'string'},
  {'key': 'state', 'data_type': 'shortString'},
  {'key': 'party', 'data_type': 'string'},
  {'key': 'currentTitle', 'data_type': 'string'}
]

# api.open.fec.gov/v1/candidate/{candidate_id}/totals
financial_summary_fields = [
  {'key': 'totalReceipts', 'data_type': 'integer'},
  {'key': 'totalDisbursements', 'data_type': 'integer'},
  {'key': 'cashOnHand', 'data_type': 'integer'},
  {'key': 'debts', 'data_type': 'integer'},
  {'key': 'lastReportDate', 'data_type': 'dateTime'}
]

# api.open.fec.gov/v1/schedules/schedule_a/by_state
geographic_contribution_fields = [
  {'key': 'state', 'data_type': 'shortString'},
  {'key': 'zipCode', 'data_type': 'shortString'},
  {'key': 'contributionAmount', 'data_type': 'integer'},
  {'key': 'contributionCount', 'data_type': 'integer'},
  {'key': 'electionYear', 'data_type': 'integer'}
]