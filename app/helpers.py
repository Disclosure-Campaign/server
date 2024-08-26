import re
from sqlalchemy import or_
from fuzzywuzzy import fuzz

from app.db.schemas.models import Politician

def split_name(raw_name):
    titles = ['Dr', 'Sr', 'Jr', 'Mr', 'Mrs', 'Iii']

    name = raw_name.title()
    name = re.sub(r'[^\w\s-]', '', name)
    parts = re.split(r'[,\s]+', name)

    name_parts = [part for part in parts if part not in titles]
    titles = [part for part in parts if part in titles]

    last_name = name_parts[0]
    first_name = name_parts[1] if len(name_parts) > 1 else ''
    middle_name = ' '.join(name_parts[2:]) if len(name_parts) > 2 else ''

    return [last_name, first_name, middle_name, titles]

def construct_name(parts):
    last_name, first_name, middle_name, titles = parts
    name = ''

    if 'Dr' in titles:
        name += 'Dr. '

    name += first_name

    if len(middle_name) > 0:
        name += f' {middle_name}'

        if len(middle_name) == 1:
            name += '.'

    name += f' {last_name}'

    if 'Iii' in titles:
        name += ' III'
    elif 'Sr' in titles:
        name += ' Sr.'
    elif 'Jr' in titles:
        name += ' Jr.'

    return name

def normalize_name(raw_name):
    return construct_name(split_name(raw_name))

def add_candidate_fields(input_politician):
    politician = input_politician.copy()

    [last_name, first_name, middle_name, titles] = split_name(politician['name'])

    politician['lastName'] = last_name
    politician['firstName'] = first_name

    politician['label'] = construct_name([last_name, first_name, middle_name, titles])
    politician['id'] = politician['fec_id']
    politician['type'] = 'politician'

    return politician


def find_politician(session, ids):
    fec_id = ids.get('fecId', 'N/A')
    opensecrets_id = ids.get('opensecretsId', 'N/A')

    politician = session.query(Politician).filter(
        or_(
            Politician.fecId1 == fec_id,
            Politician.fecId2 == fec_id,
            Politician.fecId3 == fec_id,
            Politician.opensecretsId == opensecrets_id
        )
    ).first()

    return politician

def fuzzy_match(name1, name2, threshold=80):
    return fuzz.token_sort_ratio(name1, name2) >= threshold



# def stitch(candidates, congress_members):
#     candidate_count = len(candidates)
#     unmatched_congress_member_count = len(congress_members)

#     members_by_name = {
#         normalize_name(member['name']): member for member in congress_members
#     }

#     politicians = []
#     index = 0

#     while index < candidate_count:
#         candidate = candidates[index]
#         politician = add_candidate_fields(candidate)

#         state = states[politician['state']]

#         if politician['incumbent_challenge'] == 'I':
#             candidate_name = politician['label']
#             _match = None

#             if candidate_name in members_by_name:
#                 _match = members_by_name[candidate_name]
#             else:
#                 for name in members_by_name.keys():
#                     if fuzzy_match(candidate_name, name):
#                         print(f'{candidate_name} matched with {name}')
#                         if members_by_name[name]['state'] == state:
#                             _match = members_by_name[name]

#                             break
#                         else:
#                             print('incorrect state')

#             if _match is not None:
#                 politician = politician | _match
#                 unmatched_congress_member_count -= 1
#             else:
#                 print('unmatched:')
#                 print(politician)

#         politicians.append(politician)
#         index += 1

#     print(f'unmatched congress members: {unmatched_congress_member_count}')

#     return politicians

# def combine_lists(list1, list2, key):
#     combined_list = []
#     seen_ids = set()

#     print(f'1: {len(list1)}')
#     print(f'2: {len(list2)}')

#     for item in list1 + list2:
#         if item[key] not in seen_ids:
#             combined_list.append(item)
#             seen_ids.add(item[key])
#         else:
#             print(item)

#     print(f'3: {len(combined_list)}')

#     return combined_list