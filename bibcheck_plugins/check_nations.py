# -*- coding: utf-8 -*-
from invenio.utils import NATIONS_DEFAULT_MAP


def find_nations(field, subfields):
    result = []
    for x in field:
        if x[0] in subfields:
            values = [x.replace('.', '') for x in x[1].split(', ')]
            possible_affs = filter(lambda x: x is not None,
                                   map(NATIONS_DEFAULT_MAP.get, values))
            if 'CERN' in possible_affs and 'Switzerland' in possible_affs:
                # Don't use remove in case of multiple Switzerlands
                possible_affs = [x for x in possible_affs
                                 if x != 'Switzerland']

            result.extend(possible_affs)

    result = sorted(list(set(result)))

    if result:
        return result
    else:
        return ['HUMAN CHECK']


def delete_field(field, subfield):
    field[:] = [x for x in field if x[0] != subfield]


def check_records(records, empty=False):
    fields = ['100', '700']

    for record in records:
        for field in fields:
            if field in record:
                for i, x in enumerate(record[field]):
                    data = x[0]
                    delete_field(data, 'w')
                    for val in find_nations(data, ['u', 'v']):
                        record.add_subfield((field + '__w', i, 0),
                                            'w', val)
