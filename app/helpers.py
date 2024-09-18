from flask import current_app
import hashlib
import json
import re

from sqlalchemy import or_
from sqlalchemy.inspection import inspect

from fuzzywuzzy import fuzz

from app.cache import cache
from app.db.schemas.models import Politician

ignore_cache = False

def generate_cache_key(params, key):
    sorted_params = json.dumps(params, sort_keys=True)

    hashed_params = hashlib.md5(sorted_params.encode('utf-8')).hexdigest()

    return f'{key}-{hashed_params}'

def check_cache(cache_key):
    result = None
    cached_data = cache.get(cache_key)

    if cached_data:
        current_app.logger.info(f'Cache hit for key: {cache_key}')

        result = cached_data

    return result

def use_cache(callback, params, key):
    cache_key = generate_cache_key(params, key)
    cache_data = check_cache(cache_key)

    if (cache_data is not None) and (ignore_cache is False):
        print('using cache')

        result = cache_data
    else:
        result = callback(params)

        cache.set(cache_key, result, timeout=60*60*24)

    return result

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

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

def fuzzy_match(name1, name2):
    return fuzz.token_sort_ratio(name1, name2)